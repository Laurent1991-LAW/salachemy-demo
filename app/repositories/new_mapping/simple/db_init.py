import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy.sql import func
from typing_extensions import Annotated

engine = create_engine(
    'postgresql://postgres:pwd12345678@127.0.0.1:5432/postgres', echo=True
)

Base = declarative_base()

"""
定义注解
"""
int_pk = Annotated[int, mapped_column(primary_key=True)]

timestamp_default_now = Annotated[datetime.datetime,
                                  mapped_column(nullable=False, server_default=func.now())] # 创建时间 : sql原生方法生成默认值

class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    id: Mapped[int_pk] # 使用注解
    # id: Mapped[int] =  mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    birthday: Mapped[datetime.datetime]

    create_time: Mapped[timestamp_default_now]  # 使用注解

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)