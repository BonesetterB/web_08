import pika
from mongoengine import connect, Document
from mongoengine.fields import StringField, BooleanField
import configparser
from faker import Faker

class Email(Document):
    fullname=StringField(unique=True)
    email=StringField()
    check=BooleanField(default=False)

def create_email():
    fake=Faker('uk-UA')
    config = configparser.ConfigParser()
    config.read('config.ini')

    mongo_user = config.get('DB', 'user')
    mongodb_pass = config.get('DB', 'pass')
    domain = config.get('DB', 'domain')
    db_name=config.get('DB', 'db_name')
    connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)
    email = Email(fullname=fake.name(), email=fake.email())
    email.save()
    return email._object_key['pk']

x=create_email()
print(x)

