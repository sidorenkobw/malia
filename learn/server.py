"""
Web server for driving training and testing remotely.
"""
import sys, time, socket
import cyclone.web, cyclone.sse
from twisted.internet import reactor, defer, task
from twisted.python import log
from twisted.python.filepath import FilePath
from twisted.internet import protocol

import train

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
        self.settings.trainRunner.restart()
        self.finish()

_logWatchers = {} # values are SSEHandler objects with sendEvent method
        
class TrainLogs(cyclone.sse.SSEHandler):
    def bind(self):
        self.key = time.time()
        _logWatchers[self.key] = self
        self.resync()

    def resync(self):
        self.sendEvent(event='clear', message='')
        for line in self.settings.trainRunner.recentLogs:
            self.sendEvent(event='line', message=line)
        
    def unbind(self):
        del _logWatchers[self.key]

        
class TrainRunner(object):
    def __init__(self):
        self.recentLogs = []
        task.LoopingCall(self.fake).start(1)


    def restart(self):
        train.train(self.onStep)

    def cancel(self):
        raise

    def onStep(self, lg):
        print 'step', lg
        
    def fake(self):
        line = 'line %s' % time.time()
        self.recentLogs = self.recentLogs[-10:] + [line]
        for lw in _logWatchers.values():
            lw.sendEvent(event='line', message=line)


trainRunner = TrainRunner()
log.startLogging(sys.stderr)
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
