
import streamlit as st
import pandas as pd

# Load CSV file
df = pd.read_csv(r'C:\Users\pedro\OneDrive\Documents\Taskgrok1\task1\train.csv')

# Show first rows
st.write("First rows of the file:")
st.dataframe(df.head())

# Example: total sales by region (adjust column names as needed)
if 'Region' in df.columns and 'Sales' in df.columns:
    sales_by_region = df.groupby('Region')['Sales'].sum().reset_index()
    st.write("Total sales by region:")
    st.dataframe(sales_by_region)
else:
    st.write("Columns 'Region' or 'Sales' not found in the file.")

import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('superstore.db')

# Save DataFrame as table in the database
df.to_sql('sales', conn, if_exists='replace', index=False)

# Data cleaning
st.write('---')
st.write('Data cleaning:')
st.write(f"Null values per column:\n{df.isnull().sum()}")
df = df.dropna()  # Remove rows with null values
st.write(f"After removing nulls: {df.shape[0]} rows")

# Remove outliers (example for Sales column)
q1 = df['Sales'].quantile(0.25)
q3 = df['Sales'].quantile(0.75)
iqr = q3 - q1
lower_limit = q1 - 1.5 * iqr
upper_limit = q3 + 1.5 * iqr
df = df[(df['Sales'] >= lower_limit) & (df['Sales'] <= upper_limit)]
st.write(f"After removing outliers: {df.shape[0]} rows")

# EDA: descriptive statistics
st.write('---')
st.write('Descriptive statistics:')
st.dataframe(df.describe())

# Charts with Matplotlib/Seaborn
import matplotlib.pyplot as plt
import seaborn as sns

st.write('---')
st.write('Sales distribution:')
fig, ax = plt.subplots()
sns.histplot(df['Sales'], bins=30, ax=ax)
st.pyplot(fig)

st.write('Sales by region:')
fig2, ax2 = plt.subplots()
sales_by_region = df.groupby('Region')['Sales'].sum().reset_index()
sns.barplot(x='Region', y='Sales', data=sales_by_region, ax=ax2)
st.pyplot(fig2)

# Export cleaned DataFrame to a new CSV
df.to_csv('train_clean.csv', index=False)
st.write('File train_clean.csv exported successfully!')

# Example of SQL query directly in Python
query = "SELECT Region, SUM(Sales) AS TotalSales FROM sales GROUP BY Region;"
result = conn.execute(query).fetchall()
st.write("Total sales by region (via SQL):")
st.dataframe(result)

# SQL query: total sales by category
query_category = "SELECT Category, SUM(Sales) AS TotalSales FROM sales GROUP BY Category;"
result_category = conn.execute(query_category).fetchall()
st.write("Total sales by category (via SQL):")
st.dataframe(result_category)

conn.close()