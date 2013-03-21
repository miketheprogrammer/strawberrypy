from strawberry.core.database.mongitude.base import connection, documents, schema, encoders
from bson import ObjectId
import datetime

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


    def __init__(self, *args, **kwargs):
        self._id = ObjectId
        self.username = ObjectId
        self.item = str
        self.is_liked = bool
        super(self.__class__, self).__init__(
                collection_name='user_likes',
                **kwargs)


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



class RealUserDocument(documents.RevisionedDocument):
    class Meta(object):
        required_fields = ['username']

    def __init__(self, *args, **kwargs):
        self._id = ObjectId
        self.username = str
        self.name = {
                'first':str,
                'last':str,
        }
        self.age = int
        self.likes = list
        super(self.__class__, self).__init__(collection_name='real_users', **kwargs)

