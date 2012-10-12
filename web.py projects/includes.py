#!/usr/local/bin/python2.7
import sys
import os

# fix import and weird WSGI path issues
abspath = os.path.abspath(os.path.dirname(sys.argv[0]))
parentdir = os.path.dirname(abspath)
sys.path.insert(1, parentdir)  # add current path
os.chdir(abspath)

import web
import ConfigParser
import json
import redis

# Render Engines! 
import tenjin
from tenjin.helpers import *

# redis session
import redisSessions

#config and messages
config = ConfigParser.SafeConfigParser()
config.read('config.ini')

web.config.debug = True  # set this to false when deploying (i.e. Master branch commits)

# Routes
urls = (
        # static pages get listed first
        '/', 'index',
        )

curdir = os.path.dirname(__file__)

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()

# Redis Stuff
redisServer = redis.StrictRedis()  # fill in details!

#Session stuff
session = web.session.Session(app,
                            redisSessions.RedisStore(ip='xxx.xxx.xxx.xxx',  # if you don't know IP addresses, shame on you
                                                    port=1234,  # port has to be integer
                                                    db=1,  # redis database ID, has to be integer
                                                    initialFlush=False),  # when deploying set initialFlush to true
                                                    initializer={},  # whatever the fuck you want to initialize
                                                    format='Default'  # choose 'json' if you want to mess around. 
                                                    )

# these are the default settings. Think you might want to set this up
web.config.session_parameters = web.storify({
    'cookie_name': 'webpy_session_id',  # change this to your application name
    'cookie_domain': None,
    'cookie_path' : None,
    'timeout': 86400, #24 * 60 * 60, # 24 hours in seconds
    'ignore_expiry': True,
    'ignore_change_ip': True,
    'secret_key': 'fLjUfxqXtfNoIldA0A0J',  # for all that is heavenly and good and sacred, CHANGE THIS
    'expired_message': 'Session expired',
    'httponly': True,
    'secure': False
})

# Declare your database shit. Also, make up your bloody mind, Chewxy. 
# Stop switchiing from MySQL to CouchDB to Neo4j for no good reason.


# Render Engine (tenjin rhymes with engine):
render = web.template.render('templates/', globals={
                                                    'messages': messages,
                                                    },
                                cache=False
                            )  # Templator (slow as hell)
render = tenjin.Engine(path=['templates'])  # tenjin

from views import *