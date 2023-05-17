from sqlalchemy import (create_engine, Column, Integer, String, Date)
from sqlalchemy.orm import declarative_base, sessionmaker

# Create a sqlite database named inventory.db
engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Create the Product class
class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True)
    product_name = Column('Name', String)
    product_price = Column('Price', Integer)
    product_quantity = Column('Quantity', Integer)
    date_updated = Column('Date', Date)
    
    def __repr__(self):
        return f'Name: {self.product_name} Price: {self.product_price} Quantity: {self.product_quantity} Date: {self.date_updated}'
    