"""
Web server for driving training and testing remotely.
"""
import sys, time
import cyclone.web, cyclone.sse
from twisted.internet import reactor, defer, task
from twisted.python import log
from twisted.python.filepath import FilePath

class SoundListing(cyclone.web.RequestHandler):
    def get(self):
        top = FilePath('sounds')
        self.write({'sounds': [{'path': '/'.join(p.segmentsFrom(top))} for p in sorted(top.walk()) if p.isfile()]})

class Train(cyclone.web.RequestHandler):
    def put(self):
        d = defer.Deferred()
        self.write("one\n")
        def two():
            self.write("two\n")
            d.callback(None)
        reactor.callLater(1, two)
        return d


_logWatchers = {}
        
class TrainLogs(cyclone.sse.SSEHandler):
    def bind(self):
        self.key = time.time()
        _logWatchers[self.key] = self
        for line in self.settings.trainRunner.recentLogs:
            self.sendEvent(event='line', message=line)
        
    def unbind(self):
        del _logWatchers[self.key]

        
class TrainRunner(object):
    def __init__(self):
        self.recentLogs = []
        task.LoopingCall(self.fake).start(1)

    def restart(self):
        raise

    def cancel(self):
        raise
       
        
    def fake(self):
        line = 'line %s' % time.time()
        self.recentLogs = self.recentLogs[-100:] + [line]
        for lw in _logWatchers.values():
            lw.sendEvent(event='line', message=line)


trainRunner = TrainRunner()
log.startLogging(sys.stderr)
reactor.listenTCP(
    9990,
    cyclone.web.Application([
        (r'/()', cyclone.web.StaticFileHandler, {"path": "learn", "default_filename": "index.html"}),
        (r'/lib/(.*)', cyclone.web.StaticFileHandler, {"path": "public_html/lib"}),
        (r'/sounds', SoundListing),
        (r'/sounds/(.*\.webm)', cyclone.web.StaticFileHandler, {"path": "sounds"}),
        (r'/train', Train),
        (r'/train/logs', TrainLogs),
    ], trainRunner=trainRunner))
reactor.run()
