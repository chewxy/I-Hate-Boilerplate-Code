import sys
from includes import *

try:
    print sys.argv
    PORT = int(sys.argv[1])
except IndexError:
    PORT = 8080

if __name__ == "__main__":
    if '--gevent' in sys.argv:
        from gevent import monkey; monkey.patch_all()
        from gevent.pywsgi import WSGIServer
        print('Application is now WSGI. Will run on %s' % PORT)
        WSGIServer(('', PORT), application).serve_forever()
    else:
        app.run()