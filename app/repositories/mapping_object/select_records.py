from db_init import Session, Person

session = Session()

# persons = session.query(Person).all()
persons = session.query(Person).filter(Person.address == 'HK' )

for person in persons:
    print(f"name: {person.name}, address: {person.address}")

# =========== 仨方法只取一个结果 ===========

"""
first() - 存在一条或多条, 只取第一条, 多条/没有 不会 报错
"""
result = session.query(Person).filter(Person.id < 100).first()

"""
one() - 默认只有1条, 如果有 多条/没有 会 报错
"""
    # sqlalchemy.exc.MultipleResultsFound: Multiple rows were found when exactly one was required
    # sqlalchemy.exc.NoResultFound: No row was found when one was required
# result = session.query(Person).filter(Person.id > 100).one()

"""
scalar() - 默认只有1条, 如果有 多条 会 报错; 没有 则不会
"""
# result = session.query(Person).filter(Person.id > 100).scalar()

if result:
    print(f"name: {result.name}, address: {result.address}")
