# Part 1: Ad-hoc example demonstrating pivot (wide format) and melt (long format)
import pandas as pd

# Create a simple sample dataset of sales by Region and Product
data = {
    'Region': ['North', 'North', 'South', 'South', 'East', 'East'],
    'Product': ['Apple', 'Banana', 'Apple', 'Banana', 'Apple', 'Banana'],
    'Sales': [100, 150, 80, 200, 90, 130]
}
df = pd.DataFrame(data)
# Display the original dataset
print("Original DataFrame:")
print(df)

# Use pivot_table to summarize total sales by Region and Product.
# This will group data by Region (index) and Product (columns), and aggregate Sales by sum.
pivot_df = df.pivot_table(index='Region', columns='Product', values='Sales', aggfunc='sum')
# Display the pivoted (wide format) table
print("\nPivot Table - Total Sales by Region and Product:")
print(pivot_df)

# Use melt to convert the pivot table back to long format.
# Resetting the index before melt to turn the index into a column.
melted_df = pivot_df.reset_index().melt(id_vars='Region', value_name='TotalSales', var_name='Product')
# Display the melted DataFrame (long format)
print("\nMelted DataFrame (from pivot table back to long format):")
print(melted_df.sort_values(['Region', 'Product']))

# Part 2: Real-world example using orderdetails and product data (pivot and melt in a business context)
# Load the orderdetails and product data (pipe '|' delimited CSV files)
orders = pd.read_csv('/workspaces/accpython202507/exampledata/orderdetails.csv', sep='|')
products = pd.read_csv('/workspaces/accpython202507/exampledata/product.csv', sep='|')
# Merge order details with product info to get additional fields like Color and ProductCategoryID
sales = orders.merge(products[['ProductID', 'Color', 'ProductCategoryID']], on='ProductID', how='left')
# Fill missing Color values with a placeholder (e.g., "No Color") for clarity in pivot output
sales['Color'] = sales['Color'].fillna('No Color')

# Create a pivot table to see total sales (LineTotal) by ProductCategoryID and Color.
# Index = ProductCategoryID (each product category), Columns = Color, Value = sum of LineTotal (total sales).
sales_pivot = sales.pivot_table(index='ProductCategoryID', columns='Color', values='LineTotal', aggfunc='sum', fill_value=0)
# Display the pivot table (wide format) of total sales by category and color.
print("\nPivot Table - Total Sales by Product Category and Color (first 5 categories shown):")
print(sales_pivot.head())  # Showing only the first 5 categories for brevity

# If needed, use melt to convert this pivot table back to long format for further analysis.
sales_long = sales_pivot.reset_index().melt(id_vars='ProductCategoryID', value_name='TotalSales', var_name='Color')
# Display the melted DataFrame (long format) with a few rows as example.
print("\nMelted DataFrame - Total Sales by Category/Color (first 10 rows):")
print(sales_long.head(10))







# ------------------------------------------------------------
# Pandas Demo (Pivot/Melt + .apply column-wise and row-wise)
# ------------------------------------------------------------
# This single script:
# 1) Shows a simple ad-hoc dataset to demonstrate pivot & melt basics.
# 2) Uses real-world datasets (orderdetails.csv + product.csv) to create a
#    business-style pivot table and melt it back to long form.
# 3) Demonstrates .apply *column-wise* (default axis=0) and *row-wise*
#    (axis=1) on the real-world data for practical analytics tasks.
#
# All explanations are in comments so you can run this in a notebook
# and talk through each step in roughly a 1-hour lesson.
# ------------------------------------------------------------

import pandas as pd
import numpy as np   # needed for log1p demo in .apply section

# -----------------------------------------------------------------
# PART 1  ──  Ad-hoc example: pivot_table + melt
# -----------------------------------------------------------------
data = {
    'Region':  ['North', 'North', 'South', 'South', 'East',  'East'],
    'Product': ['Apple', 'Banana', 'Apple', 'Banana', 'Apple', 'Banana'],
    'Sales':   [100, 150, 80,      200,      90,       130]
}
df = pd.DataFrame(data)
print("Ad-hoc dataset:\n", df, "\n")

# Pivot to wide format: rows = Region, columns = Product, values = Sales
pivot_df = df.pivot_table(index='Region',
                          columns='Product',
                          values='Sales',
                          aggfunc='sum')
print("Pivoted (wide) table:\n", pivot_df, "\n")

# Melt: convert the pivoted wide table back to long format
melted_df = pivot_df.reset_index().melt(id_vars='Region',
                                        value_name='TotalSales',
                                        var_name='Product')
print("Melted back to long format:\n",
      melted_df.sort_values(['Region', 'Product']), "\n")

# -----------------------------------------------------------------
# PART 2  ──  Real-world pivot & melt with orderdetails + product
# -----------------------------------------------------------------
orders   = pd.read_csv('orderdetails.csv', sep='|')
products = pd.read_csv('product.csv',     sep='|')

# Merge to bring in Color & ProductCategoryID (& StandardCost for apply demo)
cols_to_keep = ['ProductID', 'Color', 'ProductCategoryID', 'StandardCost']
sales = orders.merge(products[cols_to_keep], on='ProductID', how='left')

# Fill missing Color so pivot has explicit column; fill StandardCost with 0
sales['Color']         = sales['Color'].fillna('No Color')
sales['StandardCost']  = sales['StandardCost'].fillna(0)

# Business-style pivot: Total LineTotal $ by Category & Color
sales_pivot = sales.pivot_table(index='ProductCategoryID',
                                columns='Color',
                                values='LineTotal',
                                aggfunc='sum',
                                fill_value=0)
print("Pivot: Total sales by ProductCategoryID & Color (first 5 rows):\n",
      sales_pivot.head(), "\n")

# Melt the pivot back to long form for downstream analysis
sales_long = (sales_pivot
              .reset_index()
              .melt(id_vars='ProductCategoryID',
                    value_name='TotalSales',
                    var_name='Color'))
print("Melted (long) version of pivot (first 10 rows):\n",
      sales_long.head(10), "\n")

# -----------------------------------------------------------------
# PART 3  ──  .apply  (column-wise vs row-wise)
# -----------------------------------------------------------------
# COLUMN-WISE APPLY  (axis = 0, which is the default)
# ---------------------------------------------------
# Example A: compute mean of every numeric column in one go
numeric_cols      = sales.select_dtypes(include='number')
column_means      = numeric_cols.apply(lambda col: col.mean())
print("Column-wise .apply → mean of numeric columns:\n",
      column_means, "\n")

# Example B: transform all numeric columns in a DataFrame
# Here we build a small sample DF with only numeric columns to illustrate.
numeric_sample    = numeric_cols[['OrderQty', 'UnitPrice', 'LineTotal']]
log_transformed   = numeric_sample.apply(np.log1p)  # log1p = log(1+x)
print("Column-wise transformation with .apply (log1p):\n",
      log_transformed.head(), "\n")

# ROW-WISE APPLY  (axis = 1)
# ---------------------------------------------------
# Business scenario: compute Profit for each order line:
# Profit = LineTotal – (StandardCost * OrderQty)
sales_with_profit = sales.copy()

# Apply a lambda on each row (axis=1) that references multiple columns
sales_with_profit['Profit'] = sales_with_profit.apply(
    lambda row: row['LineTotal'] - (row['StandardCost'] * row['OrderQty']),
    axis=1
)
print("Row-wise .apply → Profit per line (cols shown):\n",
      sales_with_profit[['OrderID', 'ProductID', 'LineTotal',
                         'OrderQty', 'StandardCost', 'Profit']].head(), "\n")

# Another row-wise example: flag high-revenue lines
sales_with_profit['HighRevenueFlag'] = sales_with_profit.apply(
    lambda r: 'High' if r['LineTotal'] >= 1000 else 'Normal',
    axis=1
)
print("Row-wise .apply → HighRevenueFlag counts:\n",
      sales_with_profit['HighRevenueFlag'].value_counts(), "\n")

