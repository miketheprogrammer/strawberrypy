from schema import LoadSchema
from connection import Connection
from bson import ObjectId

class BaseDocument(object):
    class Meta(object):
        pass

    def __init__(self, *args, **kwargs):
        #consider a LoadSchema notation here
        self.schema = LoadSchema(self.__dict__.copy())
        self.fields = self.schema.__dict__.copy()

        for key in kwargs:
            if key in self.fields:
                setattr(self, key, kwargs.get(key))

        self._query = {}
        self.connection = Connection()
        self.collection_name = kwargs.get('collection_name')
        if kwargs.get('db'):
            self._db = kwargs.get('db')[self.collection_name ]
        else:
            self._db = self.connection.db[self.collection_name ]

        for k in kwargs:
            if k in self.fields:
                self._query[k] = kwargs.get(k)

        if self._query:
            self._populate_fields()



    @property
    def db(self):
        return self._db

    def get_real_query(self, query):
        return query

    @classmethod
    def find(cls, query):
        instance = cls()
        db = instance.connection.db
        query = cls(db=db).get_real_query(query)
        print query
        #rev_id = query['_revision_id']
        results = cls(db=db)._db.find(query)
        objects = []
        for result in results:
            #print result
            obj = cls(db=db)
            obj.populate_fields(result)
            if hasattr(cls.Meta, 'related_to'):
                for k, v in cls.Meta().related_to.items():
                    #print '%s : (%s,%s)' % (k,str(v[0]),v[1])
                    _results = v[0](db=db)._db.find({v[1]:getattr(obj, v[1])})
                    #print 'Result Count: %i' % _results.count()
                    for _result in _results:
                        like = v[0](db=db)
                        like.populate_fields(_result)
                        obj.likes.append(like)
            objects.append(obj)
        return objects
        #print objects
        #for i in objects:
        #    if len(i.likes) > 0:
        #        print i.likes

    def __unicode__(self):
        return self.__class__.__name__ + "_unicode"

    def prepare_fields(self):
        if type(self._id) is type(ObjectId):
            del self.fields['_id']

        for k, v in self.fields.items():
            #if not isinstance(v, type(self.schema.__dict__[k])):
            if type(self.schema.__dict__[k]) == type(v):
                print k
                print v
                try:
                    setattr(self,k,v())
                except:
                    if type(self.schema.__dict__[k]) == type(getattr(self,k)):
                        print type(v)
                        if type(v) == dict:
                            continue
                        else:
                            raise Exception(str(v) + ' Could not be converted')
    def save(self):
        if self.check_required():
            self.prepare_fields()
            result = self._db.save(self.fields, True, True)
            self.fields['_id'] = result
            self._id = result
            return True

    def __setattr__(self, name, value):
        if 'fields' not in self.__dict__:
            self.__dict__['fields'] = {}
        if name in self.fields:
            self.fields[name] = value
        self.__dict__[name] = value
        return True if self.__dict__[name] == value else False

    def _populate_fields(self):
        if self._query:
            result = self._db.find(self._query)
            if result.count() > 1:
                obj = self._db.find(self._query)[0]
            else:
                return False
            for k, v in enumerate(obj):
                setattr(self, v, obj[v])
        else:
            return False

    def check_required(self):
        if hasattr(self.Meta, 'required_fields'):
            for i in self.Meta.required_fields:
                if self.__dict__[i] is None:
                    print self.__dict__[i]
                    raise Exception('Field Required Error' + str(i) + '>', [])
            return True
        else:
            return True

    def populate_fields(self, data):
        if type(data) == type(list):
            obj_list = []
            for key, value in data:
                obj = self.__class__()
                for k, v in value:
                    setattr(self, k, v)
                obj_list.append(obj)
        for k, v in data.items():
                #if '_id' in k:
                #    v = str(v)
                setattr(self, k, v)

    def naive_validation(self):
        for k, v in self.schema.__dict__.items():
            if type(getattr(self, k)) == type(v):
                print 'validation:success'
            else:
                print 'validation:failed'

CurrentRevisions = {}

class RevisionedDocument(BaseDocument):
    _revision_id = str

    def __init__(self, *args, **kwargs):
        self._revision_id = str
        super(RevisionedDocument, self).__init__(**kwargs)
        revision = self.get_revision()
        if revision is not None:
            self._revision_id = revision['_id']

    def check_and_migrate_indexes(self):
        if hasattr(self.Meta, 'indexes'):
            information = self._db.index_information()
            indexes_missing = False
            new_indexes = []
            keys = {}
            for indice, value in information.items():
                keys[value['key'][0][0]] = (value['key'][0][1])
            for indice, value in self.Meta.indexes.items():
                if indice in keys:
                    del keys[indice]
                else:
                    new_indexes.append(indice)
            ##early exit we are not migrating
            if len(new_indexes) == 0:
                return True

            for indice in new_indexes:
                values = self.Meta.indexes[indice]
                self._db.ensure_index(
                            indice,
                            cache_for=40,
                            **values)
            return False
        return True


    @classmethod
    def migrate(cls):
        instance = cls()
        print 'Attempting to migrate: %s ' % instance.collection_name
        db = instance.connection.db
        revision = instance.get_revision(db=db)
        new_indexes = instance.check_and_migrate_indexes()
        if new_indexes and revision is not None:
            set_a = set(revision['_schema'].items())
            set_b = set(instance.schema.get_comparable().items())
            diff =  set_a - set_b
            diff2 = set_b - set_a 
            if len(diff) == 0 and len(diff2) == 0:
                print 'Found Revision: %s \n\n' % str(revision['_id'])
                return True
       
        if revision is not None:
            version = int(revision['_version']) + 1
        else:
            version = 0
        print 'Current Version: %s ' % str(version)
        _revision = RevisionHistoryDocument()
        _revision._version = version
        _revision._collection = instance.collection_name
        _revision._schema = instance.schema.get_comparable()

        _revision.save()
        print 'New Revision for: %s \n\n' % str(instance.__class__)

    def get_real_query(self, query):
        if self._revision_id == str:
            query['_revision_id'] = self.get_revision()['_id']
        else:
            query['_revision_id'] = ObjectId(self._revision_id)
        return query

    def get_revision(self, db=None):

        global CurrentRevisions

        if str(self.__class__) in CurrentRevisions:
            return CurrentRevisions[str(self.__class__)]
        else:
            if db is None:
                db = self.connection.db
            results = db.m_revisions.find({'_collection':self.collection_name}).sort('_version', -1 ).limit(1)
            revision = results[0] if results.count(True) == 1 else None
            CurrentRevisions[str(self.__class__)] = revision
            return revision

class RevisionHistoryDocument(BaseDocument):
    class Meta(object):
        required_fields = ['_version', '_collection']
        unique_together = [('_version', '_collection')]

    def __init__(self, *args, **kwargs):
        self._id = ObjectId
        self._version = int
        self._collection = str
        self._schema = dict
        super(self.__class__, self).__init__(
                collection_name='m_revisions',
                **kwargs)

    