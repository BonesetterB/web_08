import pika, sys
from mongoengine import connect
import configparser
from producer import Email
from bson import ObjectId


def main():
    credential=pika.PlainCredentials('guest','guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost',port=5672,credentials=credential))
    channel = connection.channel()

    channel.queue_declare(queue='send_email')

    def callback(ch, method, properties, body):
        email_id = ObjectId(body.decode())
        email=Email.objects(id=email_id).first()
        email.update(set__check=True)
        print('Change on True')

    channel.basic_consume(queue='send_email', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    print('Finish')

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    mongo_user = config.get('DB', 'user')
    mongodb_pass = config.get('DB', 'pass')
    domain = config.get('DB', 'domain')
    db_name=config.get('DB', 'db_name')
    connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)