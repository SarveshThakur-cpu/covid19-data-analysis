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
# 2. Load COVID grouped data
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
# 4. Select USA data
# -----------------------------------

usa = df[
    df["Country_Region"] == "US"
].copy()


print("\nUSA Data:")
print(usa.head())

print("\nUSA Dataset Shape:")
print(usa.shape)

print("\nUSA Date Range:")
print(usa["Date"].min())
print(usa["Date"].max())


# -----------------------------------
# 5. Confirmed Cases
# -----------------------------------

fig1 = px.line(
    usa,
    x="Date",
    y="Confirmed",
    title="USA - Confirmed COVID-19 Cases"
)


# -----------------------------------
# 6. Deaths
# -----------------------------------

fig2 = px.line(
    usa,
    x="Date",
    y="Deaths",
    title="USA - COVID-19 Deaths"
)


# -----------------------------------
# 7. Recovered Cases
# -----------------------------------

fig3 = px.line(
    usa,
    x="Date",
    y="Recovered",
    title="USA - Recovered COVID-19 Cases"
)


# -----------------------------------
# 8. Daily New Cases
# -----------------------------------

fig4 = px.bar(
    usa,
    x="Date",
    y="New_cases",
    title="USA - Daily New COVID-19 Cases"
)


# -----------------------------------
# 9. Cases vs Deaths
# -----------------------------------

scatter_data = usa.dropna(
    subset=["Confirmed", "Deaths"]
)

fig5 = px.scatter(
    scatter_data,
    x="Confirmed",
    y="Deaths",
    title="USA - Confirmed Cases vs Deaths",
    hover_data=["Date"]
)


# -----------------------------------
# 10. Create One Page
# -----------------------------------

fig = make_subplots(
    rows=3,
    cols=2,
    subplot_titles=[
        "USA - Confirmed COVID-19 Cases",
        "USA - COVID-19 Deaths",
        "USA - Recovered COVID-19 Cases",
        "USA - Daily New COVID-19 Cases",
        "USA - Confirmed Cases vs Deaths",
        ""
    ]
)


# -----------------------------------
# 11. Add Charts
# -----------------------------------

for trace in fig1.data:
    fig.add_trace(
        trace,
        row=1,
        col=1
    )


for trace in fig2.data:
    fig.add_trace(
        trace,
        row=1,
        col=2
    )


for trace in fig3.data:
    fig.add_trace(
        trace,
        row=2,
        col=1
    )


for trace in fig4.data:
    fig.add_trace(
        trace,
        row=2,
        col=2
    )


for trace in fig5.data:
    fig.add_trace(
        trace,
        row=3,
        col=1
    )


# -----------------------------------
# 12. Update Layout
# -----------------------------------

fig.update_layout(
    title_text="COVID-19 Country Analysis - USA",
    height=1200,
    showlegend=False
)


# -----------------------------------
# 13. Show Dashboard
# -----------------------------------

fig.show()


# -----------------------------------
# 14. Close Database Connection
# -----------------------------------

conn.close()

print("\nDatabase connection closed!")