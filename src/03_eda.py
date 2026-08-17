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
# 3. Top 10 Countries by Total Cases
# -----------------------------------

top_cases = df.sort_values(
    by="TotalCases",
    ascending=False
).head(10)


print("\nTop 10 Countries by Total Cases:")

print(
    top_cases[
        [
            "Country_Region",
            "TotalCases"
        ]
    ]
)


# -----------------------------------
# 4. Top 10 Countries by Total Deaths
# -----------------------------------

top_deaths = df.sort_values(
    by="TotalDeaths",
    ascending=False
).head(10)


print("\nTop 10 Countries by Total Deaths:")

print(
    top_deaths[
        [
            "Country_Region",
            "TotalDeaths"
        ]
    ]
)


# -----------------------------------
# 5. Top 10 Countries by Recovered
# -----------------------------------

top_recovered = df.sort_values(
    by="TotalRecovered",
    ascending=False
).head(10)


print("\nTop 10 Countries by Total Recovered:")

print(
    top_recovered[
        [
            "Country_Region",
            "TotalRecovered"
        ]
    ]
)


# -----------------------------------
# 6. Top 10 Countries by Total Tests
# -----------------------------------

top_tests = df.sort_values(
    by="TotalTests",
    ascending=False
).head(10)


print("\nTop 10 Countries by Total Tests:")

print(
    top_tests[
        [
            "Country_Region",
            "TotalTests"
        ]
    ]
)


# -----------------------------------
# 7. Close connection
# -----------------------------------

conn.close()

print("\nDatabase connection closed.")