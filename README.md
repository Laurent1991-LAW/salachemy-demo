# salachemy-demo

```shell
docker run -d \
  --name pgsql \
  -p 5432:5432  \
  -e POSTGRES_PASSWORD=pwd1-8 \
  postgres

docker exec 

psql -h localhost -p 5432 -U postgres -d postgres
```

databse: postgres
schema: sqlachemy_demo
table: 



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



# ORM

## Basic


## 一对多ORM

### 对象注入: relationship

### lazy

### 双向关联1: backref

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

### 双向关联2: backpolulate

```python
class Department(Base):
    employees: Mapped[List["Employee"]] = relationship(back_populates="department")

class Employee(Base):
    dep_id: Mapped[int] = mapped_column(ForeignKey("sqlachemy_demo.department.id")) 
    department: Mapped[Department] = relationship(lazy=False, back_populates="employees") 
```


## 多对多ORM
用户表 (类)
角色表 (类)
用户-角色关系表 (常规Table定义)


## Other Operations

### join


```python

# 1
query = select(Employee, Department).join(Employee.department, isOuter=True)

# 2
query = select(Employee, Department).select_from(outerjoin(Employee, Department))

```


### aliased


### where
- = / != / contains

## Transaction

### explicitly commit

```python
with Session(engine) as session:
    dep = Department(name="QA")
    session.add(dep)
    session.commit()
```

### Wanna avoid commit line ?

- In case of error thrown, roll back

```python
with Session(engine) as session:
    with session.begin():
        dep = Department(name="QA")
        session.add(dep)

# combine first 2 lines: 
# with Session(engine) as session, session.begin() :
```

### Multiple Sessions &  Transactions

- multiple data sources, databases
- one throws error, all sessions will rollback

```python

with Session(engine1) as session1, session1.begin(), Session(engine2) as session2, session2.begin() :
    dep = Department(name="QA")
    session1.add(dep)

    emp = Employee(name="Joey")
    session1.add(user)

```