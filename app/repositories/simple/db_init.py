import sqlalchemy
from sqlalchemy.dialects.postgresql import insert

engine = sqlalchemy.create_engine(
    'postgresql://postgres:pwd12345678@127.0.0.1:5432/postgres', echo=True
)

meta_data = sqlalchemy.MetaData(schema="sqlachemy_demo")
person_table = sqlalchemy.Table(
    "person", meta_data,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(128), unique=True, nullable=False),
    sqlalchemy.Column("birthday", sqlalchemy.Date, nullable=False),
    sqlalchemy. Column("address", sqlalchemy.String(255), nullable=True)
)

meta_data.create_all(engine)

# Define the upsert operation
stmt = insert(person_table).values([
    {"name": "Lauren", "birthday": "1991-11-22", "address": "456 Oak St"},
    {"name": "Bob", "birthday": "1991-03-22", "address": "789 Oak St"},
    {"name": "Charlie", "birthday": "1991-07-08", "address": "101 Pine St"}
])

# IMPT: stmt = stmt.on_conflict_do_nothing() —— 必须重新赋值stmt
stmt = stmt.on_conflict_do_update(
    index_elements=["name"],  # Column(s) to check for conflicts
    set_={
        "birthday": stmt.excluded.birthday,  # Correctly use `insert.excluded`
        "address": stmt.excluded.address
    }
)

with engine.connect() as conn:
    conn.execute(stmt)
    conn.commit()
