"""
Web server for driving training and testing remotely.
"""
import sys, time, socket, json, traceback
import cyclone.web, cyclone.sse
from twisted.internet import reactor, defer, task
from twisted.python import log
from twisted.python.filepath import FilePath
from twisted.internet import protocol
import numpy

import train
import keras.callbacks

def _default(obj):
    if isinstance(obj, numpy.number):
        return json.dumps(round(float(obj), ndigits=6))
    return json.JSONEncoder.default(_enc, obj)
_enc = json.JSONEncoder(default=_default)
encodeJsonIncludingNumpyTypes = _enc.encode

class SoundListing(cyclone.web.RequestHandler):
    def get(self):
        top = FilePath('sounds')
        self.write({
            'sounds': [{'path': '/'.join(p.segmentsFrom(top))} for p in sorted(top.walk()) if p.isfile()],
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
        
    def restart(self):
        sendEvent = lambda d: self.sendEvent('callback', d)
        class Cb(keras.callbacks.Callback):
            def on_batch_begin(self, batch, logs=None):
                sendEvent({'type': 'batch_begin', 'batch': batch, 'logs': logs})
            def on_batch_end(self, batch, logs=None):
                sendEvent({'type': 'batch_end', 'batch': batch, 'logs': logs})
            def on_epoch_begin(self, epoch, logs=None):
                sendEvent({'type': 'epoch_begin', 'epoch': epoch, 'logs': logs})
            def on_epoch_end(self, epoch, logs=None):
                sendEvent({'type': 'epoch_end', 'epoch': epoch, 'logs': logs})
            def on_train_begin(self, logs=None):
                sendEvent({'type': 'train_begin', 'logs': logs})
            def on_train_end(self, logs=None):
                sendEvent({'type': 'train_end', 'logs': logs})
            def set_model(self, model):
                sendEvent({'type': 'set_model'})
            def set_params(self, params):
                sendEvent({'type': 'set_params', 'params': params})
        reload(train)
        train.train(out_weights='weights.h5', callback=Cb())

    def set_model(self, *a, **kw):
        print "set_model", a, kw

    def cancel(self):
        raise

    def onStep(self, lg):
        print 'step', lg
        

trainRunner = TrainRunner()
#log.startLogging(sys.stderr)
reactor.listenTCP(
    9990,
    cyclone.web.Application([
        (r'/()', cyclone.web.StaticFileHandler,
         {"path": "learn", "default_filename": "index.html"}),
        (r'/lib/(.*)', cyclone.web.StaticFileHandler, {"path": "public_html/lib"}),
        (r'/sounds', SoundListing),
        (r'/sounds/sync', SoundsSync),
        (r'/sounds/(.*\.webm)', cyclone.web.StaticFileHandler, {"path": "sounds"}),
        (r'/train/restart', TrainRestart),
        (r'/train/logs', TrainLogs),
    ], trainRunner=trainRunner))
reactor.run()
