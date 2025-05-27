from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from db_init import engine

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"
    __table_args__ = {
        'schema': 'public'
    }

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    birthday = Column(Date, nullable=True)
    address = Column(String(255), nullable=True)


Base.metadata.create_all(engine)

