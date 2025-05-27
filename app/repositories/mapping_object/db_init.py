from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://postgres:pwd12345678@127.0.0.1:5432/postgres', echo=True
)

Session = sessionmaker(bind=engine)