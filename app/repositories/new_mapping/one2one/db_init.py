import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship
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
required_unique_name = Annotated[str, mapped_column(
    String(128), unique=True, nullable=False)]
timestamp_default_now = Annotated[datetime.datetime,
                                  mapped_column(nullable=False, server_default=func.now())] # 创建时间 : sql原生方法生成默认值

class Employee(Base):
    __tablename__ = "employee"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    id: Mapped[int_pk] # 使用注解
    name: Mapped[required_unique_name]
    computer_id: Mapped[int] = mapped_column(
        ForeignKey("sqlachemy_demo.computer.id"), nullable=True)

    computer = relationship("Computer", lazy=False, back_populates="employee")  # back_populates = 在对方类中的属性名

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'

class Computer(Base):
    __tablename__ = "computer"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    id: Mapped[int_pk]
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    serial_num: Mapped[required_unique_name]

    employee = relationship("Employee", lazy=False,
                            back_populates="computer")  # back_populates = 在对方类中的属性名
    
    def __repr__(self):
        return f'id: {self.id}, model: {self.model}'

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)