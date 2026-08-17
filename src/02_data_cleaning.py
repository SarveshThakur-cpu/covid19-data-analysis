import pandas as pd

from database import get_connection


# -----------------------------------
# 1. Connect to SQL Server
# -----------------------------------

conn = get_connection()

print("Database connected successfully!")


# -----------------------------------
# 2. Load COVID data
# -----------------------------------

query = """
SELECT *
FROM covid
"""

df = pd.read_sql(query, conn)


# -----------------------------------
# 3. Check original dataset
# -----------------------------------

print("\nOriginal Dataset Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())


# -----------------------------------
# 4. Remove unnecessary columns
# -----------------------------------

columns_to_drop = [
    "NewCases",
    "NewDeaths",
    "NewRecovered"
]

df = df.drop(
    columns=columns_to_drop,
    errors="ignore"
)


# -----------------------------------
# 5. Remove duplicate records
# -----------------------------------

df = df.drop_duplicates()


# -----------------------------------
# 6. Check cleaned dataset
# -----------------------------------

print("\nCleaned Dataset Shape:")
print(df.shape)

print("\nRemaining Columns:")
print(df.columns.tolist())

print("\nRemaining Missing Values:")
print(df.isnull().sum())


# -----------------------------------
# 7. Display cleaned data
# -----------------------------------

print("\nCleaned Data:")
print(df.head())


# -----------------------------------
# 8. Close connection
# -----------------------------------

conn.close()

print("\nDatabase connection closed.")