from db_init import engine, department, employee
from sqlalchemy import select

with engine.connect() as conn:
    # Case 1 : 获取 满足查询条件的 department与employee表 所有的列信息
    join = employee.join(department, employee.c.department_id == department.c.id)

    query_1 = select(join).where(department.c.name == "Engineering")

    # print(conn.execute(query_1).fetchall())
    # [(3, 2, 'Charlie', datetime.date(1993, 3, 3), 2, 'Engineering'), (4, 2, 'David', datetime.date(1994, 4, 4), 2, 'Engineering')]


    # Case 2: 仅获取满足join条件的employee信息
    join = employee.join(department, employee.c.department_id == department.c.id)

    query_2 = select(employee).select_from(join).where(department.c.name == "HR")

    print(conn.execute(query_2).fetchall())
    # [(1, 1, 'Alice', datetime.date(1990, 1, 1)), (2, 1, 'Bob', datetime.date(1992, 2, 2))]


