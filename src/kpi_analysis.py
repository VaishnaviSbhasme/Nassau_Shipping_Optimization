def calculate_kpis(df):
    total_shipments = len(df)

    average_lead_time = round(df["Lead Time"].mean(), 2)

    total_sales = round(df["Sales"].sum(), 2)

    gross_profit = round(df["Profit"].sum(), 2)

    return {
        "Total Shipments": total_shipments,
        "Average Lead Time": average_lead_time,
        "Total Sales": total_sales,
        "Gross Profit": gross_profit
    }