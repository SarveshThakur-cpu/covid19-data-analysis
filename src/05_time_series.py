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
# 2. Load covid_grouped data
# -----------------------------------

query = """
SELECT *
FROM covid_grouped
"""

df = pd.read_sql(query, conn)


# -----------------------------------
# 3. Convert Date column
# -----------------------------------

df["Date"] = pd.to_datetime(df["Date"])


# -----------------------------------
# 4. Dataset Information
# -----------------------------------

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nDate Range:")
print(df["Date"].min())
print(df["Date"].max())


# -----------------------------------
# 5. Global Daily New Cases
# -----------------------------------

global_daily = (
    df.groupby("Date")["New_cases"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    global_daily,
    x="Date",
    y="New_cases",
    title="Global Daily New COVID-19 Cases"
)


# -----------------------------------
# 6. Global Confirmed Cases
# -----------------------------------

global_confirmed = (
    df.groupby("Date")["Confirmed"]
    .sum()
    .reset_index()
)

fig2 = px.line(
    global_confirmed,
    x="Date",
    y="Confirmed",
    title="Global Confirmed COVID-19 Cases"
)


# -----------------------------------
# 7. Global Deaths
# -----------------------------------

global_deaths = (
    df.groupby("Date")["Deaths"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    global_deaths,
    x="Date",
    y="Deaths",
    title="Global COVID-19 Deaths"
)


# -----------------------------------
# 8. Global Recovered Cases
# -----------------------------------

global_recovered = (
    df.groupby("Date")["Recovered"]
    .sum()
    .reset_index()
)

fig4 = px.line(
    global_recovered,
    x="Date",
    y="Recovered",
    title="Global COVID-19 Recovered Cases"
)


# -----------------------------------
# 9. Create One Page
# -----------------------------------

fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=[
        "Global Daily New COVID-19 Cases",
        "Global Confirmed COVID-19 Cases",
        "Global COVID-19 Deaths",
        "Global COVID-19 Recovered Cases"
    ]
)


# -----------------------------------
# 10. Add Charts
# -----------------------------------

for trace in fig1.data:
    fig.add_trace(trace, row=1, col=1)

for trace in fig2.data:
    fig.add_trace(trace, row=1, col=2)

for trace in fig3.data:
    fig.add_trace(trace, row=2, col=1)

for trace in fig4.data:
    fig.add_trace(trace, row=2, col=2)


# -----------------------------------
# 11. Overall Layout
# -----------------------------------

fig.update_layout(
    title_text="COVID-19 Global Time Series Analysis",
    height=900,
    showlegend=False
)


# -----------------------------------
# 12. Show All Charts Together
# -----------------------------------

fig.show()


# -----------------------------------
# 13. Close Connection
# -----------------------------------

conn.close()

print("\nDatabase connection closed.")