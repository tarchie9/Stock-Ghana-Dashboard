import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# Title of the Dashboard
st.title("Ghana Stock Exchange Dashboard")

# Sidebar for Filters
st.sidebar.header("Filter Options")
selected_company = st.sidebar.selectbox(
    "Choose a Company",
    [
        "GCB Bank Limited",
        "AngloGold Ashanti",
        "CalBank Limited",
        "Ecobank Ghana",
        "Fan Milk Limited",
        "Guinness Ghana",
        "MTN Ghana",
        "Total Petroleum Ghana",
        "Unilever Ghana",
    ]
)

# Function to fetch stock data from Ghana Stock Exchange
def fetch_stock_data():
    # Replace this URL with an actual API or data source if available
    url = "https://example.com/api/ghana-stock-exchange"
    try:
        response = requests.get(url)
        data = response.json()
        return pd.DataFrame(data)
    except:
        # Sample data for demonstration purposes
        sample_data = {
            "Company": [
                "GCB Bank Limited",
                "AngloGold Ashanti",
                "CalBank Limited",
                "Ecobank Ghana",
                "Fan Milk Limited",
                "Guinness Ghana",
                "MTN Ghana",
                "Total Petroleum Ghana",
                "Unilever Ghana",
            ],
            "Price": [15.3, 100.5, 3.7, 9.2, 2.5, 6.8, 1.2, 3.6, 4.7],
            "Volume": [1000, 500, 700, 300, 800, 1200, 1500, 900, 600],
            "Change": [0.5, -1.0, 0.2, -0.3, 0.1, 0.0, -0.1, 0.2, -0.2],
        }
        return pd.DataFrame(sample_data)

# Load the data
stock_data = fetch_stock_data()

# Filter data for the selected company
company_data = stock_data[stock_data["Company"] == selected_company]

# Display Metrics
st.header(f"Performance of {selected_company}")
if not company_data.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Price (GHS)", company_data.iloc[0]["Price"])
    col2.metric("Volume", int(company_data.iloc[0]["Volume"]))
    col3.metric("Change (%)", company_data.iloc[0]["Change"])
else:
    st.write("No data available for the selected company.")

# Plotting Price Trend
st.header("Price Trend")
fig, ax = plt.subplots()
ax.plot(stock_data["Company"], stock_data["Price"], marker="o", linestyle="-")
ax.set_xlabel("Company")
ax.set_ylabel("Price (GHS)")
ax.set_title("Stock Prices of Companies on Ghana Stock Exchange")
st.pyplot(fig)

# Table of Stock Data
st.header("All Stock Data")
st.dataframe(stock_data)

# Real-time Update Button
if st.button("Refresh Data"):
    st.experimental_rerun()