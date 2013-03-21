import strawberry.core.server
from strawberry.core.database.mongitude.base import connection, documents, schema
from bson import ObjectId
import datetime
from json import JSONEncoder


class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj, **kwargs)


class UserDocument(documents.RevisionedDocument):
    class Meta(object):
        required_fields = ['username', 'device_uid']

    def __init__(self, *args, **kwargs):
        self._id = ObjectId
        self.username = str
        self.name = str
        self.age = int
        self.device_uid = str
        self.Player = object
        self.Weapons = list
        self.created_at = datetime.datetime
        self.updated_at = datetime.datetime
        super(self.__class__, self).__init__(collection_name='users', **kwargs)


class BaseController(object):
    default_message = '<<BaseController>>'
    response_headers = [('Content-type', 'text/plain')]

    def __init__(self, environ=None, start_response=None):
        if environ != None:
            print environ
            self.status = '200 OK'
            self.callback = start_response
            self.request = environ
            self.params = {}
            self.request_method = self.request['REQUEST_METHOD'].lower()

    def process(self):
        return getattr(self, self.request_method)()

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

class IndexController(BaseController):
    default_message = 'index'
    response_headers = [('Content-type', 'text/html')]

    def get(self):
        self.callback(self.status,self.response_headers)
        return """
<html>
    <form method="POST" action="http://localhost:8009/users?x=1&b=2">
        <input type="submit">SUBMIT</input>
    </form>
</html>
        """

class UserController(BaseController):
    default_message = 'no users'

    def get(self):
        print 'in controller'
        x = UserDocument()
        cursor= x.find({})
        results = []
        for document in cursor:
            results.append(document)
        print 'doing some mongo shit'
        json_response = MongoEncoder().encode(results)
        self.response_headers = [('Content-type', 'text/plain')]
        super(UserController, self).get()

        return json_response

    def post(self):
        return self.get()
        return 'GET ' + json_response



strawberry.core.server.load_route(r'',IndexController)
strawberry.core.server.load_route(r'^/users', UserController)
strawberry.core.server.server().start()