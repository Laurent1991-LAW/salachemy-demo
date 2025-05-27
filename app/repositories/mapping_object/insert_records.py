from db_init import Session, Person

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