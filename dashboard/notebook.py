import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
all_df = pd.read_csv("dashboard/used_data.csv")
 
 
genre = st.selectbox(
    label="Select city",
    options=tuple(set(all_df.customer_city))
)

 
most_selling_product = all_df.groupby('product_category_name_english').agg({
    'product_id':'count',
    'price':'sum'
}).sort_values('product_id',ascending=False)

most_profitable_product = all_df.groupby('product_category_name_english').agg({
    'product_id':'count',
    'price':'sum'
}).sort_values('price',ascending=False)
 
# plot number of daily orders (2021)
st.header('Dicoding Collection Dashboard :sparkles:')

st.subheader("Top Selling & Profitable Product Category")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="product_id", y="product_category_name_english", data=most_selling_product.head(5).reset_index(), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Most Selling Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="price", y="product_category_name_english", data=most_profitable_product.head(5).reset_index(), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales (in million)", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Most Profitable Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)