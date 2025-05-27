import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing_extensions import Annotated
from typing import List
engine = create_engine(
    'postgresql://postgres:pwd12345678@127.0.0.1:5432/postgres', echo=True
)

Base = declarative_base()

"""
定义注解
"""
int_pk = Annotated[int, mapped_column(primary_key=True)]
required_unique_name = Annotated[str, mapped_column(String(128), unique=True, nullable=False)]
timestamp_default_now = Annotated[datetime.datetime,
                                  mapped_column(nullable=False, server_default=func.now())] # 创建时间 : sql原生方法生成默认值

class Department(Base):
    __tablename__ = "department"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    id: Mapped[int_pk] 
    name: Mapped[required_unique_name]
    create_time: Mapped[timestamp_default_now]

    employees: Mapped[List["Employee"]] = relationship(back_populates="department")

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}, create_time: {self.create_time}'
    
class Employee(Base):
    __tablename__ = "employee"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    id: Mapped[int_pk]
    dep_id: Mapped[int] = mapped_column(
        ForeignKey("sqlachemy_demo.department.id")) # 若有非public的schema, 定义外键时必须specify
    name: Mapped[required_unique_name]
    birthday: Mapped[datetime.datetime] = mapped_column(nullable=False)

    """
    定义: 注入在员工类 里的 部门对象
    """
    department: Mapped[Department] = relationship(lazy=False, back_populates="employees") 
    # IMPT! 
    #   若 lazy=True 则只有代码里 明确写明 需要查获 department对象时 才会查询取回department信息
    #   但若 每次query都 必然需要 employee里的全部部门信息, lazy=True 会导致2次数据库session, 降低效率 -> lazy=True

    def __repr__(self):
        return f'id: {self.id}, dep_id: {self.dep_id}, name: {self.name}, create_time: {self.birthday}'

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)