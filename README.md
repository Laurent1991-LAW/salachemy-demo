# 1.Databse setup

```shell
docker run -d \
  --name pgsql \
  -p 5432:5432  \
  -e POSTGRES_PASSWORD=pwd1-8 \
  postgres

docker exec -it e04 psql -h localhost -p 5432 -U postgres -d postgres
```

- databse: postgres
- schema: sqlachemy_demo


# 2. Sqlachemy Basic
## 2.1. Table Creation
```python
engine = sqlalchemy.create_engine(
    'postgresql://postgres:xxx@127.0.0.1:5432/postgres', echo=True
)

meta_data = sqlalchemy.MetaData(
    schema="sqlachemy_demo"
)

person_table = sqlalchemy.Table(
    "person", meta_data,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(128), unique=True, nullable=False),
    sqlalchemy.Column("birthday", sqlalchemy.Date, nullable=False),
    sqlalchemy. Column("address", sqlalchemy.String(255), nullable=True)
)

meta_data.create_all(engine)

```

## 2.2. Insert / Upsert

```python
# Define the upsert operation
# Insert methode with Table as parameter type
stmt = insert(person_table).values([
    {"name": "Lauren", "birthday": "1991-11-22", "address": "456 Oak St"},
    {"name": "Bob", "birthday": "1991-03-22", "address": "789 Oak St"},
    {"name": "Charlie", "birthday": "1991-07-08", "address": "101 Pine St"}
])

# IMPT: stmt = stmt.on_conflict_do_nothing() —— 必须重新赋值stmt
stmt = stmt.on_conflict_do_update(
    index_elements=["name"],  # Column(s) to check for conflicts
    set_={
        "birthday": stmt.excluded.birthday,  # Correctly use `insert.excluded`
        "address": stmt.excluded.address
    }
)

with engine.connect() as conn:
    conn.execute(stmt)
    conn.commit()

```


## 2.3. Query and Update

## 2.3.1. Query Operation
- fetchall()
- fetchone()

```python
with engine.connect() as conn:
    # Select all records from the person table
    select_stmt = person_table.select()
    result = conn.execute(select_stmt)
    
    # Fetch all results
    persons = result.fetchall()
    # Fetch one result
    person = result.fetchone()

    # Print each person's details
    for person in persons:
        print(f"ID: {person.id}, Name: {person.name}, Birthday: {person.birthday}, Address: {person.address}")
```

## 2.3.2. Update / Delete Operation

```python
with engine.connect() as conn:
    update_stmt = person_table.update().values(address="123 Main St").where(
        person_table.c.name == "Lauren"
    )

    delete_stmt = person_table.delete().where(
        person_table.c.name == "Bob"
    )

    conn.execute(update_stmt)
    conn.commit()
```

## 2.3.3. Where Clause
- where function with params as conditions
- or_() / and_()

```python
    select_stmt = person_table.select().where(
        person_table.c.name != "Lauren",
        person_table.c.birthday > "1991-01-01"
    )

    # Where ... OR ... clause to filter records
    select_stmt = person_table.select().where(
        or_(
            person_table.c.name == "Lauren",
            and_(
                person_table.c.birthday > "1991-01-01",
                person_table.c.id < 7
            )
        )
    )
```

## 2.4. Multiple Tables
### 2.4.1. ForeignKey constraint
- `app/repositories/simple/one_to_many/db_init.py`
- 员工表的department_id关联部门表的Id
- 若有非public的schema, 定义外键时必须specify
```python
employee = sqlalchemy.Table(
    "employee", meta_data,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "department_id", 
        sqlalchemy.Integer, 
        sqlalchemy.ForeignKey("sqlachemy_demo.department.id"),  
        # 若有非public的schema, 定义外键时必须specify
        nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(128), nullable=False),
    sqlalchemy.Column("birthday", sqlalchemy.Date, nullable=False)
)
```

### 2.4.2. Join
- 基于 是否需要查出2张联表 的所有信息:
    - 都需要: select传入2张表的join关系
    - 只需左表: select只传左表
    
```python

with engine.connect() as conn:
    # Case 1 : 获取 满足查询条件的 department与employee表 所有的列信息
    # join = 2张表的join关系
    join = employee.join(department, employee.c.department_id == department.c.id)

    query_1 = select(join).where(department.c.name == "Engineering")

    # print(conn.execute(query_1).fetchall())
    # [(3, 2, 'Charlie', datetime.date(1993, 3, 3), 2, 'Engineering'), (4, 2, 'David', datetime.date(1994, 4, 4), 2, 'Engineering')]

    # Case 2: 仅获取满足join条件的employee信息
    join = employee.join(department, employee.c.department_id == department.c.id)

    # select方法只传入employee表, 将join关系作为参数传入select_from()方法
    query_2 = select(employee).select_from(join).where(department.c.name == "HR")

    print(conn.execute(query_2).fetchall())
    # [(1, 1, 'Alice', datetime.date(1990, 1, 1)), (2, 1, 'Bob', datetime.date(1992, 2, 2))]

```

# 3.ORM (Object-Relational Mapping)

## Session
- Different from Sqlachemy basics, ORM depends on `session` to implement DB interaction

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://postgres:xxx@127.0.0.1:5432/postgres', echo=True
)
Session = sessionmaker(bind=engine)
```

## Insert
```python
from db_init import Session, Person

# Session class defined above
session = Session()

# p = Person(name = "Joey", birthday="1980-06-16", address="HK")
# session.add(p)
session.add_all([
    Person(
        name = "Lauren", birthday = "1991-11-22", address = "GX"
    ),
    Person(
        name = "Lee", birthday = "1990-12-28", address = "CZ"
    )
])

session.commit()
```

## Select
- `session.query(TableObject).filter()`
- Retrieve one result: 
    - first()
    - one()
    - scalar()

```python

# =========== 仨方法只取一个结果 ===========

"""
first() - 存在一条或多条, 只取第一条, 多条/没有 不会 报错 
(都行, 有就给你, 没有或多了也不吱声)
"""
result = session.query(Person).filter(Person.id < 100).first()

"""
one() - 默认只有1条, 如果有 多条/没有 会 报错
(必须 == 1)
"""
    # sqlalchemy.exc.MultipleResultsFound: Multiple rows were found when exactly one was required
    # sqlalchemy.exc.NoResultFound: No row was found when one was required
result = session.query(Person).filter(Person.id > 100).one()

"""
scalar() - 默认只有1条, 如果有 多条 会 报错; 没有 则不会 
(必须 <=1)
"""
result = session.query(Person).filter(Person.id > 100).scalar()

if result:
    print(f"name: {result.name}, address: {result.address}")

```

## Update
```python
from db_init import Session
from Person import Person

session = Session()

"""
1: 查询后修改, 接着提交
"""
person = session.query(Person).filter(Person.id < 100).first()
person.address = 'updated address'

"""
2: 直接在update中update
"""
session.query(Person).filter(Person.id > 1).update({
    Person.address: "double updated address"
})

session.commit()
```
# 4.Latest Mapping Approach

## 4.1. Annotated Column Constraint
```python
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy.sql import func
from typing_extensions import Annotated

engine = create_engine(
    'postgresql://postgres:xxx@127.0.0.1:5432/postgres', echo=True
)
Base = declarative_base()

"""
定义注解
"""
int_pk = Annotated[int, mapped_column(primary_key=True)]

timestamp_default_now = Annotated[
        datetime.datetime,
        mapped_column(
            nullable=False, 
            server_default=func.now())]     # 创建时间 : sql原生方法生成默认值

class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    # 使用注解
    id: Mapped[int_pk] 
    # id: Mapped[int] =  mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    birthday: Mapped[datetime.datetime]

    create_time: Mapped[timestamp_default_now]  # 使用注解

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# =========== Insert Example ============

from db_init import Session, Customer

session = Session()
session.add(
    Customer(name="Joey", birthday="1980-06-16")
)
session.commit()

```

## 4.2. Object Inception: relationship

## 4.2.1. one2one

```python

class Employee(Base):
    __tablename__ = "employee"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    id: Mapped[int_pk]
    computer_id: Mapped[int] = mapped_column(
        ForeignKey("sqlachemy_demo.computer.id"), nullable=True)

    computer = relationship(
        "Computer", 
        lazy=False, 
        back_populates="employee")   
        # back_populates = current Class list field name in other Class definition

class Computer(Base):
    __tablename__ = "computer"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }
    employee = relationship(
        "Employee", 
        lazy=False,
        back_populates="computer") 

```

## 4.2.2. one2many
- Multiple employees in Department, using `Mapped[List["Employee"]] `

```python
class Department(Base):
    __tablename__ = "department"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    id: Mapped[int_pk] 
    employees: Mapped[List["Employee"]] = relationship(back_populates="department")
```

## 4.2.3. many2many

- using another association table to link 2 tables
- in `relationship()`, using `secondary` option to introduce association table


```python

engine = create_engine(
    'postgresql://postgres:xxx@127.0.0.1:5432/postgres', echo=True
)

Base = declarative_base(schema="sqlachemy_demo")

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

```

### 4.3. lazy

- 在员工类里
    - 若 lazy=True 则只有代码里 明确写明 需要查获 department对象时 才会查询取回department信息, 否则只有Employee表里的dep_id字段;
    - 但若 每次query都 必然需要 employee里的全部部门信息, 仍将 lazy设为True 会导致2次数据库session, 降低效率

```python

class Employee(Base):
    __tablename__ = "employee"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    id: Mapped[int_pk]
    dep_id: Mapped[int] = mapped_column(
        ForeignKey("sqlachemy_demo.department.id")) 
        # 若有非public的schema, 定义外键时必须specify
    name: Mapped[required_unique_name]
    birthday: Mapped[datetime.datetime] = mapped_column(nullable=False)

    """
    定义: 注入在员工类 里的 部门对象
    """
    department: Mapped[Department] = relationship(
        lazy=False, 
        back_populates="employees") 

```

### 4.4. Bidirectional correlation

### 4.4.1. backref
```python
class Employee(Base):
    __tablename__ = "employee"
    __table_args__ = {
        'schema': 'sqlachemy_demo'
    }

    id: Mapped[int_pk]
    dep_id: Mapped[int] = mapped_column(
        ForeignKey("sqlachemy_demo.department.id")) 
    
    """
    定义: 注入在员工类 里的 部门对象
    """
    department: Mapped[Department] = relationship(
        lazy=False, 
        backref="employees"
      ) 
```

```python
def select_department(session):
    d = session.query(Department).filter(Department.id == 1).one()
    print(d)
    print(d.employees) # 获取部门下所有的员工列表

```

缺点: 不够明确, 仅在Employee类里的department对象里有体现

### 4.4.2. back_populates

```python
class Department(Base):
    employees: Mapped[List["Employee"]] = relationship(back_populates="department")

class Employee(Base):
    dep_id: Mapped[int] = mapped_column(ForeignKey("sqlachemy_demo.department.id")) 
    department: Mapped[Department] = relationship(lazy=False, back_populates="employees") 
```
### 4.4.3. Difference
- backref只需要在一处定义, 另一层关系会自动生成; back_populates则需要在2处都声明, 后者更清晰, 对coworker更友好
- backref is a shortcut for configuring both parent.children and child.parent relationships at one place only on the parent or the child class (not both). That is :
    - instead of having:
        - `children = relationship("Child", back_populates="parent")  # on the parent class`
        - AND
        - `parent = relationship("Parent", back_populates="children")  # on the child class` 
    - you only need one of this:
        -  `children = relationship("Child", backref="parent")  # only on the parent class`
        - OR
        - `parent = relationship("Parent", backref="children")  # only on the child class`

## 4.6. Other Operations

### 4.6.1. join
- 如何配置外链接 how to configure outer join

```python
# 1 isOuter=True
query = select(Employee, Department).join(Employee.department, isOuter=True)
# 2 outerjoin()
query = select(Employee, Department).select_from(outerjoin(Employee, Department))
```

### 4.6.2. aliased

```python
emp_cls = aliased(Employee, name="emp")
dep_cls = aliased(Department, name="dep")

query = select(emp_cls, dep_cls).join(
   emp_cls.department.of_type(dep_cls))  # 若需要外连接, 可加参数 isouter=True
```

### 4.6.3. label

```python
    # query = select(Employee.name, Department.name).join_from(Employee, Department)
    # 是否加 lable 查询结果无差 | 差别在于 查询语句
    query = select(
        Employee.name.label("emp_name"), 
        Department.name.label("dep_name")).join_from(Employee, Department)
```

###  4.6.3. where
- = / != / contains
```python
dep = session.get(Department, 1)
query = select(Employee).where(Employee.department == dep)
query = select(Employee).where(Employee.department != dep)

# 获取 包含某个员工的部门 里的所有员工
emp = session.get(Employee, 1)
query = select(Department).where(Department.employees.contains(emp))
```

## 5. Transaction
### 5.1. explicitly commit
```python
with Session(engine) as session:
    dep = Department(name="QA")
    session.add(dep)
    session.commit()
```

### 5.2. Wanna avoid commit step ?
- In case of error thrown, roll back

```python
with Session(engine) as session:
    with session.begin():
        dep = Department(name="QA")
        session.add(dep)

# combine first 2 lines: 
# with Session(engine) as session, session.begin() :
```

### 5.3. Multiple Sessions &  Transactions
- multiple data sources, databases
- one throws error, all sessions will rollback

```python
with Session(engine1) as session1, session1.begin(), Session(engine2) as session2, session2.begin() :
    dep = Department(name="QA")
    session1.add(dep)

    emp = Employee(name="Joey")
    session1.add(user)
```

# 6. Others
## Python Web Structure

```plaintext
myapp/                  # 项目根目录
├── app/                # 应用核心代码（名称可自定义，如 src、backend）
│   ├── __init__.py     # 包初始化文件
│   ├── main.py         # 应用入口文件（或 app.py、server.py）
│   ├── config/         # 配置文件
│   │   ├── __init__.py
│   │   ├── default.py  # 默认配置
│   │   ├── dev.py      # 开发环境配置
│   │   └── prod.py     # 生产环境配置
│   ├── api/            # API 路由/控制器
│   │   ├── __init__.py
│   │   ├── v1/         # API 版本 1
│   │   │   ├── users.py  # 用户相关接口
│   │   │   └── posts.py  # 帖子相关接口
│   ├── models/         # 数据模型（数据库表结构）
│   │   ├── __init__.py
│   │   ├── user.py     # 用户模型
│   │   └── post.py     # 帖子模型
│   ├── services/       # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth.py     # 认证服务
│   │   └── email.py    # 邮件服务
│   ├── repositories/   # 数据访问层（与数据库交互）
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── post_repository.py
│   ├── utils/          # 工具函数和助手类
│   │   ├── __init__.py
│   │   ├── logger.py   # 日志工具
│   │   └── validators.py # 数据验证
│   └── tests/          # 测试代码
│       ├── __init__.py
│       ├── unit/       # 单元测试
│       └── integration/# 集成测试
├── migrations/         # 数据库迁移脚本（如 Alembic）
├── static/             # 静态文件（CSS、JS、图片）
├── templates/          # HTML 模板（如果使用 MVC 模式）
├── .env                # 环境变量（密钥、数据库连接等）
├── requirements.txt    # 依赖包列表
├── Dockerfile          # Docker 容器配置（可选）
├── docker-compose.yml  # 多容器配置（可选）
├── .gitignore          # Git 忽略文件
└── README.md           # 项目说明文档

```