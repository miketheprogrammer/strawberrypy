from database.mongitude.base import encoders

def serialize_list(lst):
    field_list = []
    for model in lst:
        if hasattr(model.Meta, 'related_to'):
            for k, v in model.Meta.related_to.items():
                attr = getattr(model, k)
                if isinstance(attr, list):
                    new_list = []
                    for like in attr:
                        new_list.append(like.fields)
                    setattr(model, k, new_list)
        field_list.append(model.fields)
    return encoders.MongoEncoder().encode(field_list)



