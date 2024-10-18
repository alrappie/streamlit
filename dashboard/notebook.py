import streamlit as st
import pandas as pd
import numpy as np

# Load cleaned data
all_df = pd.read_csv("./used_data.csv")
 
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
st.subheader('Daily Orders')

col1, col2 = st.columns(2)