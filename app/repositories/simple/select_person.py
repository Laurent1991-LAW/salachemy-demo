from db_init import engine, person_table

with engine.connect() as conn:
    # Select all records from the person table
    select_stmt = person_table.select()
    result = conn.execute(select_stmt)
    
    # Fetch all results
    persons = result.fetchall()
    
    # Fetch one result
    # person = result.fetchone()

    # Print each person's details
    for person in persons:
        print(f"ID: {person.id}, Name: {person.name}, Birthday: {person.birthday}, Address: {person.address}")