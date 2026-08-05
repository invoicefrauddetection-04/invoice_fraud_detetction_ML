import os
import pandas as pd
from sqlalchemy import create_engine
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db_config import DB_CONFIG

# -----------------------------------------
# PostgreSQL Connection
# -----------------------------------------

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:"
    f"{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:"
    f"{DB_CONFIG['port']}/"
    f"{DB_CONFIG['database']}"
)

engine = create_engine(DATABASE_URL)

# -----------------------------------------
# Read CSV
# -----------------------------------------

current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "..", "data", "training_invoices.csv")

df = pd.read_csv(csv_path)

print("=" * 50)
print("Dataset Loaded Successfully")
print(df.shape)
print("=" * 50)

# -----------------------------------------
# Datatype conversion 
# -----------------------------------------

boolean_columns = [
    "late_night_submission_flag",
    "blacklisted_flag",
    "is_weekend",
    "is_fraud"
]

for col in boolean_columns:
    df[col] = df[col].astype(bool)

# -----------------------------------------
# Insert into PostgreSQL
# -----------------------------------------

df.to_sql(
    name="training_invoices",
    con=engine,
    if_exists="append",
    index=False
)

print("\nData inserted successfully into PostgreSQL!")