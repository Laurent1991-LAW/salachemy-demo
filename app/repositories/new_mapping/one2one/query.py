from db_init import Session, Employee, Computer

def insert(s):
    c1 = Computer(model="Dell", serial_num="111")
    c2 = Computer(model="Surface", serial_num="222")
    c3 = Computer(model="Macbook", serial_num="333")

    e1 = Employee(name="Joey", computer=c1)
    e2 = Employee(name="Lauren", computer=c2)
    e3 = Employee(name="Lucy", computer=c3)

    s.add_all([e1,e2,e3])
    s.commit()

def select(s):
    e = s.query(Employee).filter(Employee.id == 1).one()
    if e:
        print(e)
        print(e.computer)
    
    c = s.query(Computer).filter(Computer.id == 2).one()
    if c:
        print(c)
        print(c.employee)

def update_1(s):
    s.query(Employee).filter(Employee.id == 3).update({
        Employee.computer_id: None
    })

    s.commit()

def update_2(s):
    c = s.query(Computer).filter(Computer.id == 3).scalar()
    e = s.query(Employee).filter(Employee.id == 3).scalar()

    if c and e:
        e.computer = c
        s.commit()

s = Session()
update_2(s)
