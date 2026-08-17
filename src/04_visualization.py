import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

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
# 3. Prepare data
# -----------------------------------

top15_cases = df.sort_values(
    by="TotalCases",
    ascending=False
).head(15)

top15_deaths = df.sort_values(
    by="TotalDeaths",
    ascending=False
).head(15)

top15_recovered = df.sort_values(
    by="TotalRecovered",
    ascending=False
).head(15)

top15_tests = df.sort_values(
    by="TotalTests",
    ascending=False
).head(15)

scatter_data = df.dropna(
    subset=["TotalCases", "TotalDeaths"]
)

bubble_data = df.dropna(
    subset=["TotalTests", "TotalCases"]
)


# -----------------------------------
# 4. Create individual figures
# -----------------------------------

fig1 = px.bar(
    top15_cases,
    x="Country_Region",
    y="TotalCases",
    color="TotalCases",
    title="Top 15 Countries - Total Cases"
)

fig2 = px.bar(
    top15_deaths,
    x="Country_Region",
    y="TotalDeaths",
    color="TotalDeaths",
    title="Top 15 Countries - Total Deaths"
)

fig3 = px.bar(
    top15_recovered,
    x="Country_Region",
    y="TotalRecovered",
    color="TotalRecovered",
    title="Top 15 Countries - Total Recovered"
)

fig4 = px.bar(
    top15_tests,
    x="Country_Region",
    y="TotalTests",
    color="TotalTests",
    title="Top 15 Countries - Total Tests"
)

fig5 = px.scatter(
    scatter_data,
    x="TotalCases",
    y="TotalDeaths",
    size="TotalDeaths",
    color="TotalDeaths",
    hover_data=["Country_Region", "Continent"],
    title="Total Cases vs Total Deaths"
)

fig6 = px.scatter(
    bubble_data,
    x="TotalTests",
    y="TotalCases",
    size="TotalCases",
    color="TotalCases",
    hover_data=["Country_Region", "Continent"],
    title="Total Tests vs Total Cases"
)


# -----------------------------------
# 5. Create one page with 6 charts
# -----------------------------------

fig = make_subplots(
    rows=3,
    cols=2,
    subplot_titles=[
        "Top 15 Countries - Total Cases",
        "Top 15 Countries - Total Deaths",
        "Top 15 Countries - Total Recovered",
        "Top 15 Countries - Total Tests",
        "Total Cases vs Total Deaths",
        "Total Tests vs Total Cases"
    ]
)


# -----------------------------------
# 6. Add charts to the page
# -----------------------------------

for trace in fig1.data:
    fig.add_trace(trace, row=1, col=1)

for trace in fig2.data:
    fig.add_trace(trace, row=1, col=2)

for trace in fig3.data:
    fig.add_trace(trace, row=2, col=1)

for trace in fig4.data:
    fig.add_trace(trace, row=2, col=2)

for trace in fig5.data:
    fig.add_trace(trace, row=3, col=1)

for trace in fig6.data:
    fig.add_trace(trace, row=3, col=2)


# -----------------------------------
# 7. Update overall layout
# -----------------------------------

fig.update_layout(
    title_text="COVID-19 Analysis Dashboard",
    height=1400,
    showlegend=False
)


# -----------------------------------
# 8. Show all charts together
# -----------------------------------

fig.show()


# -----------------------------------
# 9. Close database connection
# -----------------------------------

conn.close()

print("Database connection closed.")