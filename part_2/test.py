
from model import Contacts


user = Contacts.objects(pk='640f4c2e1137666b2c38d6f3')
for i in user:
    i.send_check = True
    print(i.to_mongo())
    i.save()