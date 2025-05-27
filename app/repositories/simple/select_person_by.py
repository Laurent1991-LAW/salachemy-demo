from db_init import engine, person_table
from sqlalchemy.sql import and_, or_

with engine.connect() as conn:
    # Where ... AND ... clause to filter records
    select_stmt = person_table.select().where(
        person_table.c.name != "Lauren",
        person_table.c.birthday > "1991-01-01"
    )

    # Where ... OR ... clause to filter records
    select_stmt = person_table.select().where(
        or_(
            person_table.c.name == "Lauren",
            and_(
                person_table.c.birthday > "1991-01-01",
                person_table.c.id < 7
            )
        )
    )

    result = conn.execute(select_stmt)

    result_set = result.fetchall()
    for person in result_set:
        print(
            f"ID: {person.id}, Name: {person.name}, Birthday: {person.birthday}, Address: {person.address}")
