from db_init import Session, Customer

session = Session()

session.add(
    Customer(name="Joey", birthday="1980-06-16")
)

session.commit()
