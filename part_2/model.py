from random import choice

from mongoengine import *

import faker


fake = faker.Faker("Uk_ua")

connect(host="mongodb+srv://Web9:567234@web9.3z5zqgw.mongodb.net/hw_8", ssl=True)


class Contacts(Document):
    fullname = StringField(required=True)
    email = StringField()
    phone_number = StringField()
    send_check = BooleanField(default=False)
    favorite = StringField()


def create_contact():
    """Create fake users"""

    person = Contacts(fullname=fake.name())
    person.email = fake.email()
    person.phone_number = fake.phone_number()
    person.favorite = choice(['phone', 'email'])
    person.save()