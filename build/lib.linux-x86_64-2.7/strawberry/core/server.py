from cherrypy import wsgiserver
from database.mongitude.base.documents import RevisionHistoryDocument
import re
import traceback
routes = {}
models = []
indexes = [r'', r'/', '', '/', '//', r'^', r'^/']


def load_route(route, controller):
    routes[route] = controller

def register_model(model):
    models.append(model)

def route(environ, start_response):
    try:
        path = environ['PATH_INFO']
        if path[-1:] == '/':
            path = path[:-1]

        index = None
        for route in routes:
            if re.match(route, path) and route not in indexes:
                return routes.get(route)(environ, start_response, route).process()
            elif re.match(route, path):
                index = route
        return routes.get(index)(environ, start_response).process()

    except Exception as e:
        print 'Exception'
        print e
        print traceback.format_exc()
        status = '404 NOT FOUND'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ['404 Page Not Foundx']


class server(object):
    def __init__(self, host='0.0.0.0', port=8007):
        d = wsgiserver.WSGIPathInfoDispatcher({'/': route})
        self.server = wsgiserver.CherryPyWSGIServer((host, port), d, server_name="www.m.x")

    def _prepare_system(self):
        try:
            for model in models:
                model.migrate()
        except:
            print traceback.format_exc()
            raise Exception('Error Migrating Models')

    def start(self):
        try:
            print 'Preparing Databse \n'
            self._prepare_system()
            print 'Starting Server \n'
            self.server.start()
        except KeyboardInterrupt:
            self.server.stop()