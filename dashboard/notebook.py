import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
all_df = pd.read_csv("dashboard/used_data.csv")

# Convert order_purchase_timestamp to datetime format
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

# Get min and max dates from data
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

st.header('Dicoding Collection Dashboard :sparkles:')

# Sidebar for city and date range filters
city = st.sidebar.multiselect("Select city", all_df.customer_city.unique())

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Initialize df2 with all data
df2 = all_df.copy()

# Check if both filters are applied, only one is applied, or none are applied
if city and (start_date != min_date or end_date != max_date):
    # Filter by both city and date range
    df2 = df2[df2.customer_city.isin(city)]
    df2 = df2[(df2['order_purchase_timestamp'] >= pd.Timestamp(start_date)) & 
              (df2['order_purchase_timestamp'] <= pd.Timestamp(end_date))]
    st.write(f"Filter applied: City - {city}, Date range - {start_date} to {end_date}")
    
elif city and (start_date == min_date and end_date == max_date):
    # Filter only by city
    df2 = df2[df2.customer_city.isin(city)]
    st.write(f"Filter applied: City - {city}, No date range filter applied")

elif not city and (start_date != min_date or end_date != max_date):
    # Filter only by date range
    df2 = df2[(df2['order_purchase_timestamp'] >= pd.Timestamp(start_date)) & 
              (df2['order_purchase_timestamp'] <= pd.Timestamp(end_date))]
    st.write(f"Filter applied: Date range - {start_date} to {end_date}, No city filter applied")

else:
    # No filters applied
    st.write("No filters applied")

# Calculate most selling and most profitable products
most_selling_product = df2.groupby('product_category_name_english').agg({
    'product_id': 'count',
    'price': 'sum'
}).sort_values('product_id', ascending=False)

most_profitable_product = df2.groupby('product_category_name_english').agg({
    'product_id': 'count',
    'price': 'sum'
}).sort_values('price', ascending=False)

# Plot
col1, col2 = st.columns((2))
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
with col1:
    sns.barplot(x="product_id", y="product_category_name_english", 
                data=most_selling_product.head(5).reset_index(), palette=colors, ax=ax[0])
    ax[0].set_title("Most Selling Product", fontsize=20)
    ax[0].set_xlabel("Number of Sales")

with col2:
    sns.barplot(x="price", y="product_category_name_english", 
                data=most_profitable_product.head(5).reset_index(), palette=colors, ax=ax[1])
    ax[1].set_title("Most Profitable Product", fontsize=20)
    ax[1].set_xlabel("Total Revenue")
    ax[1].invert_xaxis()

st.pyplot(fig)
