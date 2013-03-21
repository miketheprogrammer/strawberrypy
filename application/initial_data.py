from documents import UserDocument, LikesDocument, RealUserDocument
import random

for i in range(200):
    u = UserDocument()
    u.username = 'user%i' % i
    u.name = 'surname%i, first%i' % (i, i)
    u.age = i
    u.save()
    print u._revision_id
    for j in range(50):
        l = LikesDocument()
        l.username = u.username
        l.item = 'item%i' % j
        l.is_liked = random.randint(0, 49283) % 2
        l.save()
        if not isinstance(u.likes, list):
            u.likes = list()
        else:
            u.likes.append(l)

for i in range(200):
    u = RealUserDocument()
    u.username = 'user%i' % i
    u.name['first'] = 'first%i' % i
    u.name['last'] = 'last%i' % i
    u.age = i
    print u._revision_id
    u.likes = []
    for j in range(50):
        u.likes.append(
                {
                    'item':'item%i'%j,
                    'oqb':'ajdjshdie9-%i'%j
                }
            )

    u.save()

print 'Finished'
