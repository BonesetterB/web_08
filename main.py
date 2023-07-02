from mongoengine import connect, Document
from mongoengine.fields import StringField, ReferenceField,ListField
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
domain = config.get('DB', 'domain')
db_name=config.get('DB', 'db_name')

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)

class author(Document):
    fullname=StringField(unique=True)
    born_date=StringField()
    born_location=StringField()
    description=StringField()

class quotes(Document):
    tags=ListField()
    author=ReferenceField(author)
    quote=StringField()


def add_authors():
    with open('authors.json', 'r') as file:
        data = json.load(file)

    for item in data:
        authors = author(fullname=item['fullname'], born_date=item['born_date'],
                         born_location=item['born_location'],
                         description=item['description'])
        authors.save()

def add_quotes():
    with open('quotes.json', 'r') as file:
        data = json.load(file)

    for item in data:
        author_ids = [autor.id for autor in author.objects if autor.fullname == item['author']]

        quote = quotes(tags=item['tags'], author=author_ids, quote=item['quote'])
        quote.save()

def search():
    while True:
        x=input()
        if x == "exit" or x == "exit ":
            break
        x=x.split(':')
        if x[0] == 'name':
            author_name = x[1].strip()
            quote = quotes.objects.filter(author.fullname==author_name)
            for quotee in quote:
                print(quotee.quote)
        elif x[0] =='tag':
            tag = x[1].strip()
            for quote in quotes.objects:
                if tag in quote.tags:
                    print(quote.quote)
        elif x[0] == 'tags':
            tags = x[1].split(',')
            for quote in quotes.objects:
                if all(tag in quote.tags for tag in tags):
                    print(quote.quote) 
        else:
            print("unknown command")

add_authors()
add_quotes()
search()