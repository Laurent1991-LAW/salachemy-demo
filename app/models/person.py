from sqlalchemy import Column, Integer, String, MetaData, Date
from sqlalchemy.ext.declarative import declarative_base

meta_data = MetaData(schema="sqlachemy_demo")
Base = declarative_base(metadata=meta_data)

class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    birthday = Column(Date,  nullable=False)
