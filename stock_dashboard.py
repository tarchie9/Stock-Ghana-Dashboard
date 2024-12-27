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
    ["✅ Buy" if change > 1 else "❌ Sell" if change < -0.5 else "⚖️ Hold" for change in stocks_df["Change (%)"]]
)

# Streamlit App Title
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="color: green; font-size: 48px;">Ghana Stock Exchange Dashboard</h1>
        <img src="https://upload.wikimedia.org/wikipedia/commons/4/43/Ghana_Stock_Exchange_logo.jpg" alt="GSE Logo" style="width: 200px;">
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar Filters
st.sidebar.header("Filters")
sector_filter = st.sidebar.multiselect("Select Sectors:", stocks_df["Sector"].unique(), stocks_df["Sector"].unique())
price_range = st.sidebar.slider("Select Price Range (GHS):", float(stocks_df["Price"].min()), float(stocks_df["Price"].max()), (float(stocks_df["Price"].min()), float(stocks_df["Price"].max())))

# Filter data based on sidebar inputs
filtered_df = stocks_df[(stocks_df["Sector"].isin(sector_filter)) & (stocks_df["Price"].between(price_range[0], price_range[1]))]

# Recommendations Section
st.header("Stock Recommendations")
buy_recommendations = filtered_df[filtered_df["Recommendation"] == "✅ Buy"]["Company Name"].tolist()
hold_recommendations = filtered_df[filtered_df["Recommendation"] == "⚖️ Hold"]["Company Name"].tolist()
sell_recommendations = filtered_df[filtered_df["Recommendation"] == "❌ Sell"]["Company Name"].tolist()

st.markdown("### ✅ Buy Recommendations")
if buy_recommendations:
    st.write(", ".join(buy_recommendations))
else:
    st.write("No companies currently recommended for buying.")

st.markdown("### ⚖️ Hold Recommendations")
if hold_recommendations:
    st.write(", ".join(hold_recommendations))
else:
    st.write("No companies currently recommended for holding.")

st.markdown("### ❌ Sell Recommendations")
if sell_recommendations:
    st.write(", ".join(sell_recommendations))
else:
    st.write("No companies currently recommended for selling.")

# Visualization: Bar Chart of Prices
st.subheader("Stock Prices")
fig, ax = plt.subplots()
colors = ["#76c7c0" if rec == "✅ Buy" else "#f4b183" if rec == "❌ Sell" else "#d9d9d9" for rec in filtered_df["Recommendation"]]
ax.bar(filtered_df["Stock"], filtered_df["Price"], color=colors, edgecolor="black")
ax.set_ylabel("Price (GHS)")
ax.set_title("Stock Prices by Company")
st.pyplot(fig)

# Insights in Sidebar
st.sidebar.subheader("Insights")
st.sidebar.write(f"Number of Stocks: {len(filtered_df)}")
st.sidebar.write(f"Average Price: {filtered_df['Price'].mean():.2f} GHS")