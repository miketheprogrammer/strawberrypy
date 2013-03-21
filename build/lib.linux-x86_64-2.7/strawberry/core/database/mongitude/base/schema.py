class Schema(object):
    def __init__(self, schema_dict):
        del schema_dict['fields']
        self.__dict__ = schema_dict

    def apply(self, k, v):
        return self.__dict__[k](v)


    def get_comparable(self):
        copy = self.__dict__.copy()
        for k, v in copy.items():
            if 'type' in str(v):
                copy[k] = str(v)
            if 'class' in str(v):
                copy[k] = str(v)
        return copy

def LoadSchema(schema_dict):
    return Schema(schema_dict)