import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String, ForeignKey, Table, Column
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing_extensions import Annotated
from typing import List

engine = create_engine(
    'postgresql://postgres:pwd12345678@127.0.0.1:5432/postgres', echo=True
)

Base = declarative_base()

"""
user-role关联关系表
"""
association_table = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("sqlachemy_demo.users.id"), primary_key=True),
    Column("role_id", ForeignKey("sqlachemy_demo.roles.id"), primary_key=True),
)

"""
定义注解
"""
int_pk = Annotated[int, mapped_column(primary_key=True)]
required_unique_name = Annotated[str, mapped_column(String(128), unique=True, nullable=False)]
timestamp_default_now = Annotated[datetime.datetime,
                                  mapped_column(nullable=False, server_default=func.now())] # 创建时间 : sql原生方法生成默认值

"""
user表
"""
class Users(Base):
    __tablename__ = "users"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    id: Mapped[int_pk] 
    name: Mapped[required_unique_name]
    password: Mapped[str] = mapped_column(String(128), nullable=False)

    roles: Mapped[List["Roles"]] = relationship(
        secondary=association_table, 
        lazy=False,
        back_populates="users"
        )

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'


"""
role表
"""
class Roles(Base):
    __tablename__ = "roles"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    id: Mapped[int_pk]
    name: Mapped[required_unique_name]

    users: Mapped[List["Users"]] = relationship(
        secondary=association_table, 
        lazy=False,
        back_populates="roles"
        )

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)