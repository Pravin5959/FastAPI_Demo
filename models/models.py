from sqlalchemy import Column, ForeignKey, Integer, String
from database.database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    seller_id = Column(Integer, ForeignKey('sellers.sellerid'))
    seller = relationship("Seller", back_populates = 'products')

class Seller(Base):
    __tablename__ = 'sellers'
    sellerid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    products = relationship("Product", back_populates = 'seller')