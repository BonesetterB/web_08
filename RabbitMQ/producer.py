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
    email = Email(fullname=fake.name(), email=fake.email(),check=False)
    email.save()
    return str(email.id)


def main():
    for i in range(10):
        obg_id=create_email()
        channel.basic_publish(exchange='Push email', routing_key='send_email', body=obg_id)
    connection.close()

if __name__ == '__main__':
    credential=pika.PlainCredentials('guest','guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost',port=5672,credentials=credential))
    channel = connection.channel()

    channel.exchange_declare(exchange='Push email',exchange_type='direct')
    channel.queue_declare(queue='send_email')
    channel.queue_bind(exchange='Push email',queue='send_email')
    main()