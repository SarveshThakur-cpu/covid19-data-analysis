import pandas as pd

from database import get_connection


# -----------------------------------
# 1. Connect to SQL Server
# -----------------------------------

conn = get_connection()

print("Database connected successfully!")


# -----------------------------------
# 2. Load country-level data
# -----------------------------------

query = """
SELECT *
FROM covid
"""

df = pd.read_sql(query, conn)


# -----------------------------------
# 3. Basic Information
# -----------------------------------

print("\n========== DATASET INFORMATION ==========")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# -----------------------------------
# 4. Top 10 Countries by Cases
# -----------------------------------

top_cases = (
    df[
        ["Country_Region", "TotalCases"]
    ]
    .sort_values(
        by="TotalCases",
        ascending=False
    )
    .head(10)
)

print("\n========== TOP 10 COUNTRIES BY CASES ==========")

print(top_cases.to_string(index=False))


# -----------------------------------
# 5. Top 10 Countries by Deaths
# -----------------------------------

top_deaths = (
    df[
        ["Country_Region", "TotalDeaths"]
    ]
    .sort_values(
        by="TotalDeaths",
        ascending=False
    )
    .head(10)
)

print("\n========== TOP 10 COUNTRIES BY DEATHS ==========")

print(top_deaths.to_string(index=False))


# -----------------------------------
# 6. Top 10 Countries by Recovered
# -----------------------------------

top_recovered = (
    df[
        ["Country_Region", "TotalRecovered"]
    ]
    .sort_values(
        by="TotalRecovered",
        ascending=False
    )
    .head(10)
)

print("\n========== TOP 10 COUNTRIES BY RECOVERED ==========")

print(top_recovered.to_string(index=False))


# -----------------------------------
# 7. Top 10 Countries by Testing
# -----------------------------------

top_tests = (
    df[
        ["Country_Region", "TotalTests"]
    ]
    .sort_values(
        by="TotalTests",
        ascending=False
    )
    .head(10)

)

print("\n========== TOP 10 COUNTRIES BY TESTS ==========")

print(top_tests.to_string(index=False))


# -----------------------------------
# 8. Global Totals
# -----------------------------------

total_cases = df["TotalCases"].sum()

total_deaths = df["TotalDeaths"].sum()

total_recovered = df["TotalRecovered"].sum()

total_tests = df["TotalTests"].sum()


print("\n========== GLOBAL TOTALS ==========")

print("Total Cases:", int(total_cases))

print("Total Deaths:", int(total_deaths))

print("Total Recovered:", int(total_recovered))

print("Total Tests:", int(total_tests))


# -----------------------------------
# 9. Case Fatality Rate
# -----------------------------------

case_fatality_rate = (
    total_deaths / total_cases
) * 100


print("\n========== CASE FATALITY RATE ==========")

print(
    "Case Fatality Rate:",
    round(case_fatality_rate, 2),
    "%"
)


# -----------------------------------
# 10. Recovery Rate
# -----------------------------------

recovery_rate = (
    total_recovered / total_cases
) * 100


print("\n========== RECOVERY RATE ==========")

print(
    "Recovery Rate:",
    round(recovery_rate, 2),
    "%"
)


# -----------------------------------
# 11. Close Connection
# -----------------------------------

conn.close()

print("\nDatabase connection closed!")