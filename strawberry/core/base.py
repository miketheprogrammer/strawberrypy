import re
import simplejson
from bson import ObjectId
class Base(object):

    def _print(self):
        print self.__class__


class BaseController(object):
    default_message = '<<BaseController>>'
    response_headers = [('Content-type', 'text/plain')]

    def __init__(self, environ=None, start_response=None, route=r'/'):
        if environ != None:
            print environ
            self.status = '200 OK'
            self.callback = start_response
            self.request = environ
            self.params = {}
            self.path = environ['PATH_INFO']
            if self.path[-1:] == '/':
                self.path = self.path[:-1]
            self.route = re.search(route,self.path).group(0)
            self.request_method = self.request['REQUEST_METHOD'].lower()

    def process(self):
        self._process_parameters()
        return getattr(self, self.request_method)()

    def prepare_debug(self):
        for k, v in self.query.items():
            if isinstance(v, ObjectId):
                self.query[k] = str(v)
    def get_debug(self):
        self.prepare_debug()
        return ("\nQUERY :" + simplejson.dumps(self.query)
               + "\nParams :" + simplejson.dumps(self.params)
               + "\n PATH :" + simplejson.dumps(self.path)
               + "\n\n\n\n")
    def _process_parameters(self):
        params = self.path.split(self.route)[1]
        params = self.path.split('/')
        params = params[2:len(params)]
        for i in range(0, len(params), 2):
            try:
                v = int(params[i+1])
            except:
                v = str(params[i+1])
            self.params[params[i]] = v
        print self.params

    def get(self):
        self.callback(self.status,self.response_headers)
        return 'HELP'

    def post(self):
        self.callback(self.status,self.response_headers)
        return 'HELP'

    def put(self):
        self.callback(self.status,self.response_headers)
        return 'HELP'

    def parse_qs(self, querystring):
        for v in querystring.split('&'):
            p = v.split('=')
            self.params[p[0]] = p[1]
        return self.params