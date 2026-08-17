import pandas as pd

from database import get_connection


# -----------------------------------
# 1. Connect to SQL Server
# -----------------------------------

conn = get_connection()

print("Database connected successfully!")


# -----------------------------------
# 2. SQL Query
# -----------------------------------

query = """
SELECT *
FROM covid
"""


# -----------------------------------
# 3. Load SQL data into Pandas
# -----------------------------------

df = pd.read_sql(query, conn)


# -----------------------------------
# 4. Display first 5 rows
# -----------------------------------

print("\nFirst 5 rows:")
print(df.head())


# -----------------------------------
# 5. Display dataset shape
# -----------------------------------

print("\nDataset Shape:")
print(df.shape)


# -----------------------------------
# 6. Close connection
# -----------------------------------

conn.close()

print("\nDatabase connection closed.")