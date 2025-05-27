from db_init import Session, Employee, Department
from sqlalchemy import select, insert, update, delete, desc
from sqlalchemy.orm import aliased

"""
Insert
"""
def insert_records_with_relationship(session):
    d1 = Department(name="Singer")
    e1 = Employee(department=d1, name="Joey", birthday="1980-06-16")

    d2 = Department(name="Engineer")
    e2 = Employee(department=d2, name="Lauren", birthday="1991-11-22")
   
    d3 = Department(name="Logistics")
    e3 = Employee(department=d3, name="Luc", birthday="1985-10-10")

    session.add_all([e1, e2, e3])

    session.commit()


def execute_print(query): 
    result = session.execute(query)
    for row in result:
        print(row)

"""
Sing table select - order by
"""
def select_employee(session):
    query = select(Employee).order_by(Employee.id)
    # 获取倒序
    # query = select(Employee).order_by(desc(Employee.id)) 
    execute_print(query)


"""
Multiple Tables Select
"""
def select_join():
    query = select(Employee, Department).join(Employee.department)
    execute_print(query)
    # 查询结果里出现2次id - 分别为2张表的字段名
    # 但从 打印出的sql查询语句可知 采用AS关键字进行区别
    # (id: 1, dep_id: 1, name: Joey, create_time: 1980-06-16 00:00:00, id: 1, name: Singer, create_time: 2025-05-27 01:52:16.287712)

def select_join_alias():
    emp_cls = aliased(Employee, name="emp")
    dep_cls = aliased(Department, name="dep")

    query = select(emp_cls, dep_cls).join(
        emp_cls.department.of_type(dep_cls))  # 若需要外连接, 可加参数 isouter=True
    execute_print(query)
"""
配置别名后:
    SELECT emp.id, emp.dep_id, emp.name, emp.birthday, dep.id AS id_1, dep.name AS name_1, dep.create_time, department_1.id AS id_2, department_1.name AS name_2, department_1.create_time AS create_time_1
    FROM sqlachemy_demo.employee AS emp JOIN sqlachemy_demo.department AS dep ON dep.id = emp.dep_id LEFT OUTER JOIN sqlachemy_demo.department AS department_1 ON department_1.id = emp.dep_id
"""

"""
Select Specific Fields with/without customized name
"""
def select_fields():
    # query = select(Employee.name, Department.name).join_from(Employee, Department)
    # 是否加 lable 查询结果无差 | 差别在于查询语句
    query = select(
        Employee.name.label("emp_name"), 
        Department.name.label("dep_name")).join_from(Employee, Department)
    execute_print(query)

def select_from_where():
    dep = session.get(Department, 1)
    # query = select(Employee).where(Employee.department == dep)
    query = select(Employee).where(Employee.department != dep)
    execute_print(query)


def select_contains():
    emp = session.get(Employee, 1)
    query = select(Department).where(Department.employees.contains(emp))
    execute_print(query)

def batch_insert():
    session.execute(
        insert(Department).values(
            [
                {"name": "QA"},
                {"name": "Sales"},
            ]
        )
    )
    session.commit()

def batch_orm_insert():
    session.execute(
        insert(Employee).values(
            [
               {
                    "name": "Lauren Law",
                    "birthday": "1991-11-22",
                    "dep_id": select(Department.id).where(Department.name == 'Sales')
               },
               {
                    "name": "Joey Jung",
                    "birthday": "1980-06-16",
                    "dep_id": select(Department.id).where(Department.name == 'Singer')
               }  
            ]
        )
    )
    session.commit()

def batch_update():
    session.execute(
        update(Employee),
        [
            {"id": 1, "birthday": "1999-1-2"},
            {"id": 2, "name": "Samuel"}
        ]
    )
    session.commit()

def batch_delete():
    session.execute(
        delete(Employee).where(Employee.name.in_(['Luc']))
    )
    session.commit()

session = Session()
# select_join_alias()
# select_fields()
# select_from_where()
# select_contains()
# batch_insert()
batch_orm_insert()
