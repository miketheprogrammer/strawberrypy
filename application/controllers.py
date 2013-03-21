from strawberry.core.base import BaseController
from strawberry.core.database.mongitude.base import encoders
import strawberry.core.serializers
import documents



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
    collection = documents.UserDocument


    def get(self):
        self.query = self.params
        results = self.collection.find(self.query)
        json_response = strawberry.core.serializers.serialize_list(results)
        self.response_headers = [('Content-type', 'text/plain'), ('Cache-Control',('max-age=100'))]
        super(UserController, self).get()

        return self.get_debug() + json_response

    def post(self):
        return self.get()
        return 'GET ' + json_response

class LikesController(BaseController):
    default_message = 'no users'
    collection = documents.LikesDocument

    def get(self):
        self.query = self.params
        results = self.collection.find(self.query)
        json_response = strawberry.core.serializers.serialize_list(results)
        self.response_headers = [('Content-type', 'text/plain')]
        super(LikesController, self).get()
        return self.get_debug() + json_response

    def post(self):
        return self.get()
        return 'GET ' + json_response

class RealUserController(BaseController):
    default_message = 'no users'
    collection = documents.RealUserDocument

    def get(self):
        self.query = self.params
        results = self.collection.find(self.query)
        json_response = strawberry.core.serializers.serialize_list(results)
        self.response_headers = [('Content-type', 'text/plain')]
        super(RealUserController, self).get()
        return self.get_debug() + json_response

    def post(self):
        return self.get()
        return 'GET ' + json_response