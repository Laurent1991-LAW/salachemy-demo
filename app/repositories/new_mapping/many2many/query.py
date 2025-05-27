from db_init import Session, Users, Roles

def insert_records(s):
    r1 = Roles(name="Admin")
    r2 = Roles(name="Operator")
    r3 = Roles(name="Mediator")

    u1 = Users(name="Joey", password="123")
    u2 = Users(name="Lauren", password="123")
    u3 = Users(name="John", password="123")

    u1.roles.append(r1)
    u1.roles.append(r2)
    u1.roles.append(r3)

    u2.roles.append(r2)
    u2.roles.append(r3)

    u3.roles.append(r3)

    s.add_all([u1, u2, u3])
    s.commit()


def insert_user(s):
    u = s.query(Users).filter(Users.id == 1).one()
    print(u)
    print(u.roles)


def insert_role(s):
    r = s.query(Roles).filter(Roles.id == 3).one()
    print(r)
    print(r.users)

s = Session()
insert_role(s)
