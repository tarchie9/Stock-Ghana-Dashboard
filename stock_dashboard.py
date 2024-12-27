import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample dataset (Simulated GSE data)
data = {
    "Stock": ["MTNGH", "GCB", "UNIL", "ETI", "TOTAL"],
    "Price": [2.45, 6.35, 17.99, 0.31, 13.12],
    "Change (%)": [1.5, -0.8, 2.3, 0.5, -0.3],
    "Volume": [100000, 50000, 20000, 150000, 80000],
    "Sector": ["Telecom", "Banking", "Consumer Goods", "Banking", "Energy"],
}

# Convert to DataFrame
stocks_df = pd.DataFrame(data)

# Add simple moving average and recommendations
stocks_df["SMA_5"] = stocks_df["Price"] * (1 + pd.Series([0.01, -0.02, 0.03, 0.00, -0.01]))
stocks_df["Recommendation"] = pd.Series(
    ["Buy" if change > 1 else "Sell" if change < -0.5 else "Hold" for change in stocks_df["Change (%)"]]
)

# Streamlit App Title
st.title("Ghana Stock Market Dashboard")

# Display Data Table
st.header("Stock Data")
st.dataframe(stocks_df)

# Interactive Filter
st.sidebar.header("Filters")
sector_filter = st.sidebar.multiselect("Select Sectors:", stocks_df["Sector"].unique(), stocks_df["Sector"].unique())

# Filter data
filtered_df = stocks_df[stocks_df["Sector"].isin(sector_filter)]

# Visualization: Bar Chart of Prices
st.subheader("Stock Prices")
fig, ax = plt.subplots()
ax.bar(filtered_df["Stock"], filtered_df["Price"], color="skyblue", edgecolor="black")
ax.set_ylabel("Price (GHS)")
ax.set_title("Stock Prices by Company")
st.pyplot(fig)

# Recommendations Visualization
st.subheader("Recommendations")
colors = {"Buy": "green", "Hold": "blue", "Sell": "red"}
recommendation_colors = [colors[rec] for rec in filtered_df["Recommendation"]]
fig, ax = plt.subplots()
ax.scatter(filtered_df["Stock"], filtered_df["Price"], color=recommendation_colors, s=100, edgecolor="black")
ax.set_ylabel("Price (GHS)")
ax.set_title("Stock Recommendations")
st.pyplot(fig)

# Add Insights
st.sidebar.subheader("Insights")
st.sidebar.write(f"Number of Stocks: {len(filtered_df)}")
st.sidebar.write(f"Average Price: {filtered_df['Price'].mean():.2f} GHS")
st.sidebar.write(f"Recommendations: {filtered_df['Recommendation'].value_counts().to_dict()}")