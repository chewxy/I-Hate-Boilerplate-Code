import sys
import argparse
from includes import *

parser = argparse.ArgumentParser(description='Run the webapp!')
parser.add_argument('-p', '--port', 
                    type=int, 
                    default=8080,
                    help='What port you want to run the web app in? You need sudo if you want to run on port 80')
parser.add_argument('-g', '--gevent', action='store_true',
                    help='Do you want to run this on a gevent server?')

args = parser.parse_args()

if __name__ == "__main__":
    if args.gevent:
        from gevent import monkey; monkey.patch_all()
        from gevent.pywsgi import WSGIServer
        print('Application is now WSGI. Will run on %s' % args.port)
        WSGIServer(('', args.port), application).serve_forever()
    else:
        sys.argv[1] = str(args.port)  # terrible hack to accomodate web.py's sys.argv[1] argument for port
        app.run()