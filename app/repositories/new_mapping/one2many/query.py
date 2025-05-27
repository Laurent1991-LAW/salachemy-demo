from db_init import Session, Employee, Department

def insert_records(session):
    d1 = Department(name="hr")
    session.add(d1)

    # IMPT! 必须flush 下方才能成功拿到d1.id
    session.flush()

    e1 = Employee(dep_id=d1.id, name="Joey", birthday="1980-06-16")
    session.add(e1)

    session.commit()


def insert_records_with_relationship(session):
    d2 = Department(name="Engineer")
    e2 = Employee(department=d2, name="Lauren", birthday="1991-11-22")
    # 只需要insert员工对象即可
    session.add(e2)

    session.commit()

def select_employee(session):
    e = session.query(Employee).filter(Employee.id == 1).one()
    print(e)
    print(e.department)


def select_department(session):
    d = session.query(Department).filter(Department.id == 1).one()
    print(d)
    print(d.employees)

s = Session()
# insert_records_with_relationship(s)
select_department(s)
