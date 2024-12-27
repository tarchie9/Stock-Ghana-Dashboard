import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Dataset of GSE-listed companies
data = {
    "Stock": ["MTNGH", "GCB", "UNIL", "EGH", "TOTAL", "SOGEGH", "SIC", "SCB", "GOIL", "GGBL"],
    "Company Name": ["MTN Ghana", "GCB Bank", "Unilever Ghana", "Ecobank Ghana", "TotalEnergies Marketing Ghana",
                     "Societe Generale Ghana", "SIC Insurance Company", "Standard Chartered Bank Ghana",
                     "Ghana Oil Company", "Guinness Ghana Breweries"],
    "Sector": ["Telecom", "Banking", "Consumer Goods", "Banking", "Oil & Gas",
               "Banking", "Insurance", "Banking", "Oil & Gas", "Consumer Goods"],
    "Price": [2.45, 6.35, 17.99, 5.25, 13.12, 7.50, 0.85, 21.00, 8.00, 6.50],
    "Change (%)": [1.5, -0.8, 2.3, 0.5, -0.3, 1.2, -0.5, 0.8, 1.1, 1.7],
    "Volume": [100000, 50000, 20000, 150000, 80000, 60000, 30000, 120000, 110000, 70000]
}

# Convert to DataFrame
stocks_df = pd.DataFrame(data)

# Add recommendations based on Change (%)
stocks_df["Recommendation"] = pd.Series(
    ["Buy" if change > 1 else "Sell" if change < -0.5 else "Hold" for change in stocks_df["Change (%)"]]
)

# Streamlit App Title
st.title("Ghana Stock Market Dashboard")

# Display Data Table
st.header("GSE-Listed Companies")
st.dataframe(stocks_df)

# Sidebar Filters
st.sidebar.header("Filters")
sector_filter = st.sidebar.multiselect("Select Sectors:", stocks_df["Sector"].unique(), stocks_df["Sector"].unique())
price_range = st.sidebar.slider("Select Price Range (GHS):", float(stocks_df["Price"].min()), float(stocks_df["Price"].max()), (float(stocks_df["Price"].min()), float(stocks_df["Price"].max())))

# Filter data based on sidebar inputs
filtered_df = stocks_df[(stocks_df["Sector"].isin(sector_filter)) & (stocks_df["Price"].between(price_range[0], price_range[1]))]

# Display Filtered Data Table
st.header("Filtered Stock Data")
st.dataframe(filtered_df)

# Visualization: Bar Chart of Prices
st.subheader("Stock Prices")
fig, ax = plt.subplots()
ax.bar(filtered_df["Stock"], filtered_df["Price"], color="skyblue", edgecolor="black")
ax.set_ylabel("Price (GHS)")
ax.set_title("Stock Prices by Company")
st.pyplot(fig)

# Recommendations Visualization
st.subheader("Stock Recommendations")
colors = {"Buy": "green", "Hold": "blue", "Sell": "red"}
recommendation_colors = [colors[rec] for rec in filtered_df["Recommendation"]]
fig, ax = plt.subplots()
ax.scatter(filtered_df["Stock"], filtered_df["Price"], color=recommendation_colors, s=100, edgecolor="black")
ax.set_ylabel("Price (GHS)")
ax.set_title("Stock Recommendations")
st.pyplot(fig)

# Insights in Sidebar
st.sidebar.subheader("Insights")
st.sidebar.write(f"Number of Stocks: {len(filtered_df)}")
st.sidebar.write(f"Average Price: {filtered_df['Price'].mean():.2f} GHS")
st.sidebar.write(f"Recommendations: {filtered_df['Recommendation'].value_counts().to_dict()}")