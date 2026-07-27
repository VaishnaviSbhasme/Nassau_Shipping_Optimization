import pandas as pd
import plotly.express as px

def ship_mode_chart(df):
    ship_mode = (
        df.groupby("Ship Mode")
        .size()
        .reset_index(name="Shipments")
    )

    fig = px.pie(
        ship_mode,
        names="Ship Mode",
        values="Shipments",
        title="Ship Mode Distribution"
    )

    return fig