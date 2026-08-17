import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from database import get_connection


# ==========================================
# 1. Database Connection
# ==========================================

conn = get_connection()

print("Database connected successfully!")


# ==========================================
# 2. Load Country-Level Data
# ==========================================

query_country = """
SELECT *
FROM covid
"""

country_df = pd.read_sql(query_country, conn)


# ==========================================
# 3. Load Date-Wise Data
# ==========================================

query_grouped = """
SELECT *
FROM covid_grouped
"""

time_df = pd.read_sql(query_grouped, conn)


# ==========================================
# 4. Convert Date
# ==========================================

time_df["Date"] = pd.to_datetime(time_df["Date"])


# ==========================================
# 5. Calculate KPIs
# ==========================================

total_cases = country_df["TotalCases"].sum()

total_deaths = country_df["TotalDeaths"].sum()

total_recovered = country_df["TotalRecovered"].sum()

total_tests = country_df["TotalTests"].sum()


case_fatality_rate = (
    total_deaths / total_cases
) * 100


recovery_rate = (
    total_recovered / total_cases
) * 100


# ==========================================
# 6. Top 10 Countries by Cases
# ==========================================

top_cases = (
    country_df[
        ["Country_Region", "TotalCases"]
    ]
    .sort_values(
        by="TotalCases",
        ascending=False
    )
    .head(10)
)


# ==========================================
# 7. Global Time Series
# ==========================================

global_daily = (
    time_df
    .groupby("Date")
    .agg({
        "Confirmed": "sum",
        "Deaths": "sum",
        "Recovered": "sum"
    })
    .reset_index()
)


# ==========================================
# 8. Cases Chart
# ==========================================

fig_cases = px.bar(
    top_cases,
    x="Country_Region",
    y="TotalCases",
    title="Top 10 Countries by COVID-19 Cases"
)


# ==========================================
# 9. Global Trend Chart
# ==========================================

fig_trend = go.Figure()

fig_trend.add_trace(
    go.Scatter(
        x=global_daily["Date"],
        y=global_daily["Confirmed"],
        mode="lines",
        name="Confirmed"
    )
)

fig_trend.add_trace(
    go.Scatter(
        x=global_daily["Date"],
        y=global_daily["Deaths"],
        mode="lines",
        name="Deaths"
    )
)

fig_trend.add_trace(
    go.Scatter(
        x=global_daily["Date"],
        y=global_daily["Recovered"],
        mode="lines",
        name="Recovered"
    )
)

fig_trend.update_layout(
    title="Global COVID-19 Trends",
    xaxis_title="Date",
    yaxis_title="Cases"
)


# ==========================================
# 10. Cases vs Deaths
# ==========================================

scatter_df = country_df.dropna(
    subset=["TotalCases", "TotalDeaths"]
)


fig_scatter = px.scatter(
    scatter_df,
    x="TotalCases",
    y="TotalDeaths",
    size="TotalDeaths",
    hover_name="Country_Region",
    title="Total Cases vs Total Deaths"
)


# ==========================================
# 11. Create Dashboard
# ==========================================

fig = make_subplots(
    rows=4,
    cols=2,

    specs=[
        [
            {"type": "indicator"},
            {"type": "indicator"}
        ],
        [
            {"type": "indicator"},
            {"type": "indicator"}
        ],
        [
            {"type": "xy", "colspan": 2},
            None
        ],
        [
            {"type": "xy"},
            {"type": "xy"}
        ]
    ],

    subplot_titles=[
        "Total Cases",
        "Total Deaths",
        "Total Recovered",
        "Total Tests",
        "Top 10 Countries by Cases",
        "",
        "Global COVID-19 Trends",
        "Cases vs Deaths"
    ]
)


# ==========================================
# 12. KPI Cards
# ==========================================

fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_cases,
        title={"text": "Total Cases"}
    ),
    row=1,
    col=1
)


fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_deaths,
        title={"text": "Total Deaths"}
    ),
    row=1,
    col=2
)


fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_recovered,
        title={"text": "Total Recovered"}
    ),
    row=2,
    col=1
)


fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_tests,
        title={"text": "Total Tests"}
    ),
    row=2,
    col=2
)


# ==========================================
# 13. Add Top Countries Chart
# ==========================================

for trace in fig_cases.data:

    fig.add_trace(
        trace,
        row=3,
        col=1
    )


# ==========================================
# 14. Add Global Trend
# ==========================================

for trace in fig_trend.data:

    fig.add_trace(
        trace,
        row=4,
        col=1
    )


# ==========================================
# 15. Add Scatter Plot
# ==========================================

for trace in fig_scatter.data:

    fig.add_trace(
        trace,
        row=4,
        col=2
    )


# ==========================================
# 16. Dashboard Layout
# ==========================================

fig.update_layout(

    title_text="COVID-19 Global Analysis Dashboard",

    height=1400,

    showlegend=True,

    template="plotly_white"
)


# ==========================================
# 17. Show Dashboard
# ==========================================

fig.show()


# ==========================================
# 18. Close Connection
# ==========================================

conn.close()

print("Database connection closed!")