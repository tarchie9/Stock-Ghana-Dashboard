import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# Title of the Dashboard
st.title("Ghana Stock Exchange Dashboard")

# Function to fetch all companies and stock data from GSE-API
def fetch_stock_data():
    url = "https://dev.kwayisi.org/apis/gse/live"  # API endpoint
    try:
        response = requests.get(url)
        data = response.json()
        # Convert data to a DataFrame
        df = pd.DataFrame(data)
        # Rename columns for better readability
        df = df.rename(columns={"name": "Symbol", "price": "Price", "volume": "Volume", "change": "Change"})
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Load stock data
stock_data = fetch_stock_data()

if not stock_data.empty:
    # Populate dropdown with all available companies
    st.sidebar.header("Filter Options")
    selected_company = st.sidebar.selectbox("Choose a Company", stock_data["Symbol"].unique())
   
    # Filter data for the selected company
    company_data = stock_data[stock_data["Symbol"] == selected_company]

    # Display Metrics for the Selected Company
    st.header(f"Performance of {selected_company}")
    if not company_data.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Price (GHS)", company_data.iloc[0]["Price"])
        col2.metric("Volume", int(company_data.iloc[0]["Volume"]))
        col3.metric("Change (%)", company_data.iloc[0]["Change"])
    else:
        st.write("No data available for the selected company.")

    # Plotting Price Trend for All Companies
    st.header("Price Trend")
    fig, ax = plt.subplots()
    ax.plot(stock_data["Symbol"], stock_data["Price"], marker="o", linestyle="-")
    ax.set_xlabel("Company")
    ax.set_ylabel("Price (GHS)")
    ax.set_title("Stock Prices of Companies on Ghana Stock Exchange")
    st.pyplot(fig)

    # Display Full Stock Data Table
    st.header("All Stock Data")
    st.dataframe(stock_data)
else:
    st.write("No data available. Please check your internet connection or try again later.")

# Real-time Update Button
if st.button("Refresh Data"):
    st.experimental_rerun()
