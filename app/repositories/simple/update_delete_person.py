from db_init import engine, person_table

with engine.connect() as conn:
    update_stmt = person_table.update().values(address="123 Main St").where(
        person_table.c.name == "Lauren"
    )

    delete_stmt = person_table.delete().where(
        person_table.c.name == "Bob"
    )

    conn.execute(update_stmt)
    conn.commit()
