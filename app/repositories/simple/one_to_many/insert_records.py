from db_init import engine, department, employee
from sqlalchemy import insert

with engine.connect() as conn:
    conn.execute(department.insert().values([
        {"name": "HR"},
        {"name": "Engineering"},
        {"name": "Marketing"}
    ]))

    conn.execute(employee.insert().values([
        {"department_id": 1, "name": "Alice", "birthday": "1990-01-01"},
        {"department_id": 1, "name": "Bob", "birthday": "1992-02-02"},
        {"department_id": 2, "name": "Charlie", "birthday": "1993-03-03"},
        {"department_id": 2, "name": "David", "birthday": "1994-04-04"},
        {"department_id": 3, "name": "Eve", "birthday": "1995-05-05"}
    ]))

    conn.commit()