import pandas as pd

def route_analysis(df):
    route_summary = (
        df.groupby("Route")["Sales"]
        .agg(["sum", "count"])
        .reset_index()
    )

    route_summary.columns = ["Route", "Total Sales", "Total Shipments"]

    route_summary = route_summary.sort_values(
        by="Total Sales",
        ascending=False
    )

    return route_summary