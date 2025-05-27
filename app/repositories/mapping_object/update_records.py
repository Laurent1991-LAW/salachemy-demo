from db_init import Session
from Person import Person

session = Session()

"""
1: 查询后修改, 接着提交

person = session.query(Person).filter(Person.id < 100).first()
person.address = 'updated address'
"""

session.query(Person).filter(Person.id > 1).update({
    Person.address: "double updated address"
})


session.commit()


