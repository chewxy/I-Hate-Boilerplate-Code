from includes import *
from methods import *


class static:
    def GET(self, name):
        return open('static/%s' % name)
