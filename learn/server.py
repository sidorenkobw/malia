"""
Web server for driving training and testing remotely.
"""
from __future__ import division
import sys, time, socket, json, traceback, urllib, datetime, tempfile
import cyclone.web, cyclone.sse
from twisted.internet import reactor, defer, task
from twisted.python import log
from twisted.python.filepath import FilePath
from twisted.internet import protocol
import numpy

import train
import keras.callbacks
import speechmodel

def _default(obj):
    if isinstance(obj, numpy.number):
        return json.dumps(round(float(obj), ndigits=6))
    if isinstance(obj, FilePath):
        return json.dumps(obj.path)
    return json.JSONEncoder.default(_enc, obj)
_enc = json.JSONEncoder(default=_default)
encodeJsonIncludingNumpyTypes = _enc.encode

userForId = {
    '13EubbAsOYgy3eZX4LAHsB5Hzq72': 'donna',
    '8WO9WnJj80SP6WRdbIZh4IxgPP82': 'drewpca',
    '4WGnHLHt9CbiOdaqOVAJGzbW2QP2': '4W?',
    '4GGUPEPZYNahAwZpQSG6n4QIR913': '4G?',
}

def soundFields(segments):
    d = {}
    if segments[0] == 'incoming':
        if len(segments) > 1:
            d['user'] = userForId.get(segments[1], segments[1])
        if len(segments) > 2:
            d['word'] = urllib.unquote(segments[2])
        if segments[2].endswith('.webm'):
            # old format
            d['word'], m = segments[2].split('_', 1)
            d['milli'] = int(m.split('.')[0])
        elif len(segments) > 3:
            d['milli'] = int(segments[3].replace('.webm', ''))
        if 'milli' in d:
            d['iso'] = datetime.datetime.fromtimestamp(d['milli'] / 1000).isoformat('T').split('.')[0]
    return d

class SoundListing(cyclone.web.RequestHandler):
    def get(self):
        top = FilePath('sounds')
        self.write({
            'sounds': [{
                'path': '/'.join(p.segmentsFrom(top)),
                'fields': soundFields(p.segmentsFrom(top)),
            } for p in sorted(top.walk()) if p.isfile()],
            'hostname': socket.gethostname(),
        })

class SoundsSync(cyclone.web.RequestHandler):
    @cyclone.web.asynchronous
    def put(self):
        req = self
        class StreamOutput(protocol.ProcessProtocol):
            def outReceived(self, data):
                req.write(data)
            def errReceived(self, data):
                req.write(data)
            def processEnded(self, status):
                req.finish()
        reactor.spawnProcess(StreamOutput(), 'make', ['/usr/bin/make', 'sync_sound_files'])

class TrainRestart(cyclone.web.RequestHandler):
    def put(self):
        try:
            self.settings.trainRunner.restart()
        except Exception:
            self.set_status(500)
            self.write({'exc': traceback.format_exc()})
            return

class ModelPlot(cyclone.web.RequestHandler):
    def get(self):
        reload(speechmodel)
        model = speechmodel.makeModel()
        out = tempfile.NamedTemporaryFile(suffix='.svg')
        plot(model, to_file=out.name, show_shapes=True)

        self.set_header('Content-Type', 'image/svg+xml')
        with open(out.name) as o:
            self.write(o.read())


_logWatchers = {} # values are SSEHandler objects with sendEvent method
        
class TrainLogs(cyclone.sse.SSEHandler):
    def bind(self):
        self.key = time.time()
        _logWatchers[self.key] = self
        self.resync()

    def resync(self):
        self.sendEvent(event='clear', message='')
        for (ev, msg) in self.settings.trainRunner.recentLogs:
            self.sendEvent(event=ev, message=msg)
        
    def unbind(self):
        del _logWatchers[self.key]

        
class TrainRunner(object):
    def __init__(self):
        self.recentLogs = []
        self.sendEvent('line', {'line': 'TrainRunner initialized'})

    def sendEvent(self, event, messageDict):
        message = encodeJsonIncludingNumpyTypes(messageDict)
        self.recentLogs = self.recentLogs[-100:] + [(event, message)]
        for lw in _logWatchers.values():
            lw.sendEvent(event=event, message=message)
            lw.transport.doWrite()
        
    def restart(self):
        sendEvent = lambda d: self.sendEvent('callback', d)
        params = {
            'sound_cur': 0, 'sound_total': 0,
            'epoch_cur': 0, 'epoch_total': 0,
            'batch_cur': 0, 'batch_total': 5,
            'acc': 0,
            'loss': 1,
            'val_acc': 0,
            'val_loss': 1,
        }
        class Cb(keras.callbacks.Callback):
            def loaded_sound(self, cur, total):
                params['sound_cur'] = cur
                params['sound_total'] = total
                sendEvent({'params': params})
            def set_model(self, model):
                pass#sendEvent({'type': 'set_model'})
            def set_params(self, train_params):
                if train_params['nb_sample'] == 0:
                    # TF makes a weird failure for this
                    raise ValueError("no samples")
                params['nb_sample'] = train_params['nb_sample']
                params['epoch_cur'] = 0
                params['epoch_total'] = train_params['nb_epoch']
                sendEvent({'type': 'set_params', 'params': params})
            def on_train_begin(self, logs=None):
                sendEvent({'type': 'train_begin'})
            def on_train_end(self, logs=None):
                sendEvent({'type': 'train_end'})
            def on_epoch_begin(self, epoch, logs=None):
                sendEvent({'params': params})
            def on_epoch_end(self, epoch, logs=None):
                params['epoch_cur'] = epoch + 1
                params.update(logs)
                sendEvent({'params': params, 'type': 'epoch_end'})
            def on_batch_end(self, batch, logs=None):
                params['batch_cur'] = batch + 1
                params['acc'] = logs['acc']
                params['loss'] = logs['loss']
                sendEvent({'params': params})
            def on_save(self, path):
                sendEvent({'type': 'save', 'path': path})
        reload(train)
        train.train(out_weights='weights.h5', callback=Cb())
        
    def cancel(self):
        raise


trainRunner = TrainRunner()
#log.startLogging(sys.stderr)
reactor.listenTCP(
    9990,
    cyclone.web.Application([
        (r'/()', cyclone.web.StaticFileHandler,
         {"path": "learn", "default_filename": "index.html"}),
        (r'/([^/]+\.html)', cyclone.web.StaticFileHandler,
         {"path": "learn"}),
        (r'/lib/(.*)', cyclone.web.StaticFileHandler,
         {"path": "public_html/lib"}),
        (r'/sounds', SoundListing),
        (r'/sounds/sync', SoundsSync),
        (r'/sounds/(.*\.webm)', cyclone.web.StaticFileHandler,
         {"path": "sounds"}),
        (r'/train/restart', TrainRestart),
        (r'/train/logs', TrainLogs),
        (r'/model/plot', ModelPlot),
    ], trainRunner=trainRunner))
reactor.run()
