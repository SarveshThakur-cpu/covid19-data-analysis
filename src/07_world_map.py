import pandas as pd
import plotly.graph_objects as go

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
# 5. Get unique dates
# -----------------------------------

dates = sorted(df["Date"].unique())


# -----------------------------------
# 6. Create Initial Data
# -----------------------------------

initial_date = dates[0]

initial_data = df[
    df["Date"] == initial_date
]


# -----------------------------------
# 7. Create Figure
# -----------------------------------

fig = go.Figure()


# -----------------------------------
# 8. Confirmed Cases Map
# -----------------------------------

fig.add_trace(
    go.Choropleth(
        locations=initial_data["iso_alpha"],
        z=initial_data["Confirmed"],
        text=initial_data["Country_Region"],
        colorscale="Blues",
        colorbar=dict(
            title="Confirmed Cases",
            x=0.45
        ),
        geo="geo",
        name="Confirmed Cases",
        visible=True
    )
)


# -----------------------------------
# 9. Deaths Map
# -----------------------------------

fig.add_trace(
    go.Choropleth(
        locations=initial_data["iso_alpha"],
        z=initial_data["Deaths"],
        text=initial_data["Country_Region"],
        colorscale="Reds",
        colorbar=dict(
            title="Deaths",
            x=1.0
        ),
        geo="geo2",
        name="Deaths",
        visible=True
    )
)


# -----------------------------------
# 10. Create Animation Frames
# -----------------------------------

frames = []

for date in dates:

    date_data = df[
        df["Date"] == date
    ]

    frames.append(
        go.Frame(
            name=str(date.date()),
            data=[
                go.Choropleth(
                    locations=date_data["iso_alpha"],
                    z=date_data["Confirmed"],
                    text=date_data["Country_Region"],
                    colorscale="Blues",
                    geo="geo"
                ),

                go.Choropleth(
                    locations=date_data["iso_alpha"],
                    z=date_data["Deaths"],
                    text=date_data["Country_Region"],
                    colorscale="Reds",
                    geo="geo2"
                )
            ]
        )
    )


fig.frames = frames


# -----------------------------------
# 11. Layout
# -----------------------------------

fig.update_layout(

    title="Global COVID-19 Confirmed Cases vs Deaths",

    height=650,

    geo=dict(
        domain=dict(
            x=[0, 0.48],
            y=[0.15, 1]
        ),
        projection_type="natural earth",
        showframe=False
    ),

    geo2=dict(
        domain=dict(
            x=[0.52, 1],
            y=[0.15, 1]
        ),
        projection_type="natural earth",
        showframe=False
    ),

    updatemenus=[
        {
            "type": "buttons",
            "showactive": False,
            "x": 0.45,
            "y": 0.05,
            "buttons": [
                {
                    "label": "▶ Play",
                    "method": "animate",
                    "args": [
                        None,
                        {
                            "frame": {
                                "duration": 150,
                                "redraw": True
                            },
                            "transition": {
                                "duration": 0
                            }
                        }
                    ]
                },
                {
                    "label": "⏸ Pause",
                    "method": "animate",
                    "args": [
                        [None],
                        {
                            "frame": {
                                "duration": 0,
                                "redraw": False
                            },
                            "mode": "immediate"
                        }
                    ]
                }
            ]
        }
    ],

    sliders=[
        {
            "active": 0,
            "x": 0.15,
            "y": 0,
            "len": 0.7,
            "currentvalue": {
                "prefix": "Date: "
            },
            "steps": [
                {
                    "label": str(date.date()),
                    "method": "animate",
                    "args": [
                        [str(date.date())],
                        {
                            "mode": "immediate",
                            "frame": {
                                "duration": 0,
                                "redraw": True
                            },
                            "transition": {
                                "duration": 0
                            }
                        }
                    ]
                }
                for date in dates
            ]
        }
    ]
)


# -----------------------------------
# 12. Show Figure
# -----------------------------------

fig.show()


# -----------------------------------
# 13. Close Connection
# -----------------------------------

conn.close()

print("\nDatabase connection closed!")