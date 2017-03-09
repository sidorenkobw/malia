"""
Web server for driving training and testing remotely.
"""
import sys
import cyclone.web
from twisted.internet import reactor, task
from twisted.python import log
from twisted.python.filepath import FilePath

class SoundListing(cyclone.web.RequestHandler):
    def get(self):
        top = FilePath('sounds')
        self.write({'sounds': [{'path': '/'.join(p.segmentsFrom(top))} for p in sorted(top.walk()) if p.isfile()]})

log.startLogging(sys.stderr)
reactor.listenTCP(
    9990,
    cyclone.web.Application([
        (r'/()', cyclone.web.StaticFileHandler, {"path": "learn", "default_filename": "index.html"}),
        (r'/lib/(.*)', cyclone.web.StaticFileHandler, {"path": "public_html/lib"}),
        (r'/sounds', SoundListing),
        (r'/sounds/(.*\.webm)', cyclone.web.StaticFileHandler, {"path": "sounds"}),
    ]))
reactor.run()
