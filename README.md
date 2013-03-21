Strawberry Py
---------------

Strawberry Py is a lightweight RESTFull (No Auth Yet) API Server. It is fast, efficient, and simple. Thats all.

This version of Strawberry Py also includes my MongoDB Relational Mapper and schema versioner called Mongitude

While both StrawberryPy and Mongitude are far from finished they sport some interesting functionality.

Installing
----------
- MUST HAVE MONGO DB INSTALLED
- clone the repo
- `git clone git@github.com:miketheprogrammer/strawberrypy.git`
	- `cd strawberrypy`
- run `sudo python setup.py install`
	- This will install dependencies [CherryPy, PyMongo]


Starting the Server
-------------------
There is a demo application in the application folder
- run `python application/start.py`
- wait for it to start then exit out of it, softly with cntr + c
- run `python application/initial_data.py`
- run `python application/start.py`

Reason for this is we need to do an initial schema migration.
After which we can load data.


The Request
-----------
Example GET Request

- `http://localhost:8007/users/` GETS all users

	The Response ( this reponse is truncated because it was way too long. Also it has debug enabled so it prints the query data)
	------------
	- `
QUERY :{"_revision_id": "5100489086a955305e447047"}
Params :{"_revision_id": "5100489086a955305e447047"}
 PATH :"/users"

`EXAMPLE ONLY Displays user0`
```PYTHON
[
	{
		"username": "user0", 
		"_revision_id": "5100489086a955305e447047", 
		"name": "surname0, first0", 
		"age": 0, 
		"_id": "5100489386a95530739473bc", 
		"likes": 
			[
				{
					"username": "user0", 
					"item": "item0", 
					"is_liked": 1, 
					"_id": "5100489386a95530739473bd", 
					"_revision_id": "5100489086a955305e447048"
				}, 
				{
					"username": "user0", 
					"item": "item1", "is_liked": 0, 

					.......etcetera
```

Tightening the search
-----------
Example GET Request

- `http://localhost:8007/users/username/user0` 
	- `Returns a subset of the users where username = user0`

Following the object hierarchy
------------------------------
We see that users have likes attributed between them and an item, thats interesting
What if we want to find all items that the user has liked

- `http://localhost:8007/likes/username/user0/is_liked/1`

	The Response ()
	------------
	```PYTHON
	[
		{
			"username": "user0", 
			"item": "item0", 
			"is_liked": 1, 
			"_id": "5100489386a95530739473bd", 
			"_revision_id": "5100489086a955305e447048"}, 
		{
			"username": "user0", 
			"item": "item4", 
			"is_liked": 1, 
			"_id": "5100489386a95530739473c1", 
			"_revision_id": "5100489086a955305e447048"}, 
		{
			"username": "user0", 
			"item": "item6", 
			"is_liked": 1, 
			"_id": "5100489386a95530739473c3", 
			"_revision_id": "5100489086a955305e447048"}, 
	]
	```

Creating a new Model or known in Strawberry as a Document.
---------------------------------------------------------

- Necessary Imports
```PYTHON
from strawberry.core.database.mongitude.base import connection, documents, schema, encoders
from bson import ObjectId

- Creating the User Document
```
```PYTHON
class UserDocument(documents.RevisionedDocument):
    class Meta(object):
        required_fields = ['username']
        related_to = {'likes': (LikesDocument, 'username')}
        indexes = {'username':
                            {
                                'name':'_username_idx_',
                                'unique':True,
                                'dropDups':True,
                            },
                  }

    def __init__(self, *args, **kwargs):
        self._id = ObjectId
        self.username = str
        self.name = str
        self.age = int
        self.likes = list
        super(self.__class__, self).__init__(collection_name='users', **kwargs)

```

Understanding the Document
--------------------------
All documents have a `class Meta(object)` which describes important information
including relational structure
- Understanding Meta
	- related_to : `related_to = {'likes': (LikesDocument, 'username')}`
		- In this case it indicates this class has a child likes composed of a document LikesDocument, related on field `username`
	- indexes : `Creates indexes on the keys listed, all parameters are natural pymongo and in turn mongo db parameters`


- Understanding __init__
	- Each field declared here is a description of schema, in order for naive-validation to work, the field must be equal to its type

	- super...blah...collection_name='users'
		- Says to use db.users as the collection. i.e. `main.users`



Example of Multiple indexes
---------------------------
```PYTHON
class LikesDocument(documents.RevisionedDocument):
    class Meta(object):
        required_fields = []
        indexes = {'username':
                            {
                                'name':'_username_idx_',
                                'unique':False,
                                'dropDups':False,
                            },
                    'item': {
                                'name':'_item_idx_',
                                'unique':False,
                                'dropDups':False
                            },
                    'is_liked': {
                                'name':'_isliked_idx_',
                                'unique':False,
                                'dropDups':False
                            },
                  }
```

- Composite Indexes are not supported yet.


CREATING a controller
---------------------

```PYTHON
from strawberry.core.base import BaseController
from strawberry.core.database.mongitude.base import encoders
import strawberry.core.serializers
import documents
```

```PYTHON
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
```

UNDERSTANDING a controller
--------------------------
```PYTHON
class UserController(BaseController):
    default_message = 'no users'
    collection = documents.UserDocument
```
	- default_message: What message to display if there are no records found.
	- collection : the model to use

```PYTHON
    def get(self):
        self.query = self.params
        results = self.collection.find(self.query)
        json_response = strawberry.core.serializers.serialize_list(results)
        self.response_headers = [('Content-type', 'text/plain'), ('Cache-Control',('max-age=100'))]
        super(UserController, self).get()
```
	- Refer to 
		```PYTHON
		results = self.collection.find(self.query)
		```
		- This call returns a collection of documents as objects, not as json

	- Refer to the line
		```PYTHON
		json_response = strawberry.core.serializers.serialize_list(results)
		```
		- Included in strawberry is a special serializer for converting between objects and mongodb.


Creating a new Application
--------------------------
 
```BASH
mkdir appname
cd appname
touch controllers.py
touch documents.py
touch start.py
```

CREATING start.py
-----------------
Assumes you have controllers and documents

```PYTHON
import strawberry
import controllers
import documents

strawberry.core.server.load_route(r'',controllers.IndexController)
strawberry.core.server.load_route(r'^/users', controllers.UserController)
strawberry.core.server.load_route(r'^/likes', controllers.LikesController)
strawberry.core.server.load_route(r'^/realusers', controllers.RealUserController)

strawberry.core.server.register_model(documents.UserDocument)
strawberry.core.server.register_model(documents.LikesDocument)
strawberry.core.server.register_model(documents.RealUserDocument)

strawberry.core.server.server(host='0.0.0.0', port=80).start()
```

UNDERSTANDING start.py
----------------------

`load_route` takes a regexp route, and a controller to use

`register_model` simply registers the model for use, and will automatically migrate all registered models.

`server().start()`
	- default host is `0.0.0.0`
	- default port is `8007`
``




