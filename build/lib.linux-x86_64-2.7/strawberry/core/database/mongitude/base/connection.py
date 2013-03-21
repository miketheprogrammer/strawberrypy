from pymongo import MongoClient


class Connection(object):
    def __init__(
        self,
        host='127.0.0.1',
        port=27017,
        maxcached=10,
        maxconnections=50,
        pool_id='default_async_pool',
        db_name='main'):

        self.host = host
        self.port = port
        self.maxcached = maxcached
        self.maxconnections = maxconnections
        self.pool_id = pool_id
        self._db_name = db_name
        self._db = None
        self.driver = None

    """
    Selects a database for use with the connection.
    """
    def select_db(self, db_name='mongitude_db'):
        self._db_name = db_name
        self._db = None

    @property
    def db(self):
        if self._db == None:
        	self._db = MongoClient()[self._db_name]
        return self._db

    
