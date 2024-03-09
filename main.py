import json
import datetime
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale


user = ''
password = ''
host = 'localhost'
port = '5432'
database = ''

DSN = f'postgresql://{user}:{password}@{host}:{port}/{database}'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as f:
    data = json.load(f)

for record in data:
    model = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

def sale_publisher(publisher=input('Введите название или идентификатор издателя: ')):
    
    selective_data = session.query(Book.title, Shop.name, Sale.price, 
                            Sale.count, Sale.date_sale).\
                            join(Publisher, Publisher.id == Book.id_publisher).\
                            join(Stock, Stock.id_book == Book.id).\
                            join(Shop, Shop.id == Stock.id_shop).\
                            join(Sale, Sale.id_stock == Stock.id)
    if publisher[0].isalpha():
        filter_result = selective_data.filter(Publisher.name == publisher)
                            
        for title, name, price, count, date_sale in filter_result:
            print(f'{title:^50} | {name:^30} | {float(price) * count:^10} | '
                  f'{date_sale.strftime("%d-%m-%Y"):^10}')
    
    elif publisher.isdigit():
        filter_result = selective_data.where(Publisher.id == int(publisher))

        for title, name, price, count, date_sale in filter_result:
            print(f'{title:^50} | {name:^30} | {float(price) * count:^10} | '
                  f'{date_sale.strftime("%d-%m-%Y"):^10}')

session.close()

if __name__ == '__main__':
    sale_publisher()