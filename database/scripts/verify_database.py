from sqlalchemy import create_engine, text
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db_config import DB_CONFIG

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:"
    f"{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:"
    f"{DB_CONFIG['port']}/"
    f"{DB_CONFIG['database']}"
)

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:

    result = connection.execute(
        text("SELECT COUNT(*) FROM training_invoices;")
    )

    count = result.scalar()

    print("=" * 50)
    print(f"Total Records : {count}")
    print("=" * 50)