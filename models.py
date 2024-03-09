import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(50), nullable=False)


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(50), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)
    
    publisher = relationship('Publisher', backref='book')
                

class Shop(Base):
    __tablename__ ='shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(50), nullable=False)

                
class Stock(Base):
    __tablename__ ='stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref='Stock')
    shop = relationship(Shop, backref='Stock')

    
class Sale(Base):
    __tablename__ ='sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.String(10), nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref='Sale')

    
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)