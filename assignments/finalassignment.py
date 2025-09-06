# Final Project: Stock Data Analysis with Pandas and Polygon API

# Overview:
# In this final exercise, you will perform a comprehensive real-world data analysis using **Pandas** on stock price data 
# retrieved from the Polygon.io API. You will pick a few stock tickers of your choice (for example, AAPL for Apple, MSFT for Microsoft, etc.) 
# and fetch their historical price data over a specified date range. Using this data, you will demonstrate proficiency in various 
# important Pandas operations: data cleaning, merging/joining, grouping, time series manipulation (resampling and rolling), 
# calculating new fields, and visualization. By the end of this project, you will have a comparative analysis of the chosen stocks 
# and practice all major Pandas functionalities in the process.

# Guidelines:
# - **Environment**: Use your GitHub Codespaces environment (or Jupyter Notebook) for this project. Make sure to install any required libraries.
# - **Data Source**: We will use Polygon.io's REST API for stock aggregates (Open/High/Low/Close, Volume) data. You have been provided an API key below.
# - **Libraries**: Aside from Python's built-in modules, you'll primarily use `pandas` for data handling. We will also use `requests` (or Polygon's client) to fetch data from the API, and `matplotlib` for plotting.
# - **Choosing Tickers**: Select **3-5 stock tickers** that you are interested in (e.g., 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'). Ensure they have sufficient historical data for the chosen period.
# - **Date Range**: Define a date range for analysis (for example, one year or two years of data). You can use a recent period (e.g., Jan 1, 2022 through Jan 1, 2023) or any period of interest. Make sure the range covers days where the market is open to get data (weekends/holidays will return no data for those dates).
# - **Polygon API Usage**: We will use the "Aggregates (Custom Bars)" endpoint to get daily OHLC data for each ticker. The general endpoint format is:  
#   `https://api.polygon.io/v2/aggs/ticker/<TICKER>/range/1/day/<START_DATE>/<END_DATE>?adjusted=true&sort=asc&limit=5000&apiKey=<YOUR_API_KEY>`  
#   We will use the provided API key in our code. If using the official Polygon Python client instead of raw requests, you would first install it (`pip install polygon-api-client`) and then use its methods to get aggregates.
# - **PIP Install**: If any of the required libraries (`pandas`, `requests`, `matplotlib`, `polygon-api-client`) are not available in your environment, install them using pip. For example:  
#   `!pip install pandas requests matplotlib polygon-api-client`  
#   (In a Codespaces or Jupyter notebook, prefix with `!`. In a regular terminal, drop the `!`. Note: Pandas and requests are likely pre-installed.)
# - **Proceed Step-by-Step**: Follow the steps below, writing code for each part. Try to think through how to accomplish each task with Pandas before coding. Use Pandas documentation or previous lessons for reference if needed.

# **Instructions:**

# **1. Setup and Data Retrieval**
#    a. **Import Libraries**: Import pandas (as pd), requests, and matplotlib's pyplot (as plt). If you installed the Polygon API client and wish to use it, import the RESTClient from polygon as well.  
#    b. **API Key**: Store the provided Polygon API key in a variable (e.g., `API_KEY = "dIUMbUHa3jguPZ9WiF5HUgIS4FWhPWlq"`). **Important**: Keep your API keys secure; avoid exposing them in public repositories. In this exercise, we use a provided key for convenience.  
#    c. **Choose Tickers and Dates**: Create a list of ticker symbols for the stocks you want to analyze. Also define your start date and end date for data collection (in format "YYYY-MM-DD"). For example: `tickers = ["AAPL", "MSFT", "GOOGL"]` and `start_date = "2022-01-01"`, `end_date = "2023-01-01"`.  
#    d. **Fetch Data for Each Ticker**: For each ticker in your list, make an API request to retrieve daily aggregate (OHLCV) data for that ticker and date range. You can use the `requests` library to GET the URL mentioned above. Check the response status and parse the JSON. The JSON will contain a list of results (each with keys like `o, h, l, c, v, t, etc.`). Extract the results and load them into a pandas DataFrame.  
#    e. **DataFrame Creation**: Create a DataFrame for each ticker's data. Each DataFrame will contain columns for timestamp, open, high, low, close, volume, etc. Name these DataFrames meaningfully (e.g., `df_aapl`, `df_msft`, ...), or store them in a dictionary keyed by ticker symbol for convenience.  
#    f. **Pause & Inspect**: Print out the first few rows (`df.head()`) of one or two of the DataFrames to ensure data was loaded correctly. Also check the number of rows (`len(df)`) to confirm you have data roughly matching the trading days in your date range.

# **2. Data Cleaning and Preparation**
#    a. **Timestamp to Datetime**: The Polygon data uses timestamps in milliseconds (`t` field) for each bar's start time. Convert this timestamp to a human-readable date. In pandas, you can convert a Unix timestamp (in ms) using `pd.to_datetime(df['t'], unit='ms')`. Create a new column (e.g., 'Date') from this conversion.  
#    b. **Rename Columns**: For better clarity, rename the columns `o, h, l, c, v` to `Open, High, Low, Close, Volume` respectively. You can use `df.rename(columns={ ... }, inplace=True)`. Also rename the timestamp column `t` to "Date" (since you created the Date column, you might drop 't' afterwards). If there are other columns like `vw` (volume-weighted price) or `n` (number of transactions) and you do not need them, you can drop those to simplify the dataset (`df.drop(columns=[...], inplace=True)`).  
#    c. **Set Date as Index** (optional at this stage): You may choose to set the new 'Date' column as the DataFrame index using `df.set_index('Date', inplace=True)`. This can make time-series operations easier later. However, if you plan to merge data from multiple tickers, you might wait and set the index after merging. We will handle indexing after combining the data.  
#    d. **Add Ticker Column**: Add a column to each DataFrame indicating the ticker symbol, e.g., `df_aapl['Ticker'] = 'AAPL'`. This will be useful when combining the data to know which row belongs to which stock.  
#    e. **Repeat for All Tickers**: Ensure all your individual ticker DataFrames have the 'Date' column (as datetime), renamed columns, and a 'Ticker' identifier column. Check each DataFrame's `head()` to confirm changes.  

# **3. Combining Data from Multiple Stocks**
#    a. **Concatenate DataFrames**: Now combine the data from all chosen tickers into one DataFrame for easier comparative analysis. Use `pd.concat([...])` to stack the DataFrames vertically. For example: `combined_df = pd.concat([df_aapl, df_msft, df_googl], ignore_index=True)`. If you stored DataFrames in a dictionary, you can use `pd.concat(list_of_dfs)`. Set `ignore_index=True` to reset the row index.  
#    b. **Verify Combined Data**: The combined DataFrame should have a column for 'Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', etc., and number of rows = sum of rows of individual DataFrames. Print `combined_df.head()` and `combined_df.tail()` to see that multiple tickers' data are present.  
#    c. **Sort Data**: It’s often useful to sort the combined DataFrame by date (and by ticker within date). Use `combined_df.sort_values(by=["Date", "Ticker"], inplace=True)` to sort primarily by date. Sorting ensures chronological order which is important for time series analysis.  
#    d. **Reset Index** (optional): If you had set Date as index earlier for individual frames, after concatenation you may need to call `combined_df.reset_index(drop=True)` to get a flat index. Alternatively, if each had Date index, you could use `pd.concat(..., axis=0)` which will preserve Date index—make sure to handle index properly as needed. For simplicity, you can keep Date as a normal column in combined_df for now.

# **4. Exploratory Data Analysis (EDA) and Descriptive Statistics**
#    a. **Basic Statistics**: Use Pandas to get basic statistics for each stock. For example, using the combined DataFrame, you can group by 'Ticker': `combined_df.groupby('Ticker')['Close'].describe()` to get count, mean, std, min, max, etc. for the closing price of each stock. Alternatively, use aggregate functions: `combined_df.groupby('Ticker')['Close'].agg(['mean','min','max','std'])`. Print the results to see the differences between stocks.  
#    b. **Overall Volume Comparison**: Find out which stock had the highest total trading volume in the period. You can do `combined_df.groupby('Ticker')['Volume'].sum()`. Similarly, find the average daily volume for each stock with `.mean()`. This tells you which stock is most traded in your dataset.  
#    c. **Daily Price Differences**: Add a new column to the combined DataFrame for each row that shows the difference between the day's close and open: `combined_df['DailyChange'] = combined_df['Close'] - combined_df['Open']`. This absolute change can be interesting, but also consider percentage change. You can add another column `combined_df['DailyPctChange'] = (combined_df['Close'] - combined_df['Open']) / combined_df['Open'] * 100` to see daily change in percentage. (Alternatively, when we set up a time series per stock, we'll calculate daily returns another way; but this is a quick per-row calc.)  
#    d. **Up vs Down Days**: Determine how often each stock closed higher than it opened (a positive "up" day). Create a boolean column `combined_df['UpDay'] = combined_df['Close'] > combined_df['Open']`. This column is True for days the stock went up. Using this, calculate the proportion of up-days for each stock: group by 'Ticker' and take the mean of 'UpDay' (since True=1, False=0, the average will be the fraction of days that are True). For example: `combined_df.groupby('Ticker')['UpDay'].mean() * 100` will give the percentage of days each stock rose. Identify which stock had the highest percentage of up-days.  
#    e. **Highest/Lowest Days**: Using the combined data, find the date and value of the highest closing price for each stock, and the lowest closing price for each stock. There are several ways: One way is group by ticker and use `.agg({'Close': ['max','min']})` to get the extreme values, but to get the date of those, you might do: `idx_max = combined_df.groupby('Ticker')['Close'].idxmax()` which gives the index (row) of the max Close per group. Then you can retrieve the 'Date' at those indices. Similarly for idxmin. Print out each stock's peak price and date, and lowest price and date.  
#    f. **Print EDA Results**: As you compute these, use `print()` statements to output the results in a readable format (you can format strings to show ticker name and value, or just print the Pandas result objects which are nicely formatted). This will help in understanding the dataset before moving on.

# **5. Pivoting and Time-Series Alignment**
#    a. **Pivot to Wide Format**: For many analyses, it's useful to have dates as index and each stock's values in separate columns (wide format). Create a pivot table or use Pandas pivot function to achieve this. For example, to get closing prices in wide format: `price_df = combined_df.pivot(index='Date', columns='Ticker', values='Close')`. This will produce a DataFrame where the index is the Date, and there is one column per ticker containing the Close price.  
#    b. **Review Pivoted Data**: Inspect `price_df.head()`; you should see date indices and multiple columns (one for each ticker's close). The Date index may not be sorted if the original combined data wasn't sorted by date, so ensure it's sorted: `price_df.sort_index(inplace=True)`. If you set the Date as index earlier and did an outer join, you could also use `pd.concat` with axis=1 as an alternative method to get a similar wide dataframe, but pivot is straightforward here.  
#    c. **Handling Missing Dates**: If your date range includes non-trading days, the pivot will have gaps (missing dates) where no data (NaN) appears for all stocks (e.g., weekends, holidays), or in some cases one stock might be NaN on a date where another has data (if one stock started trading later). For simplicity, you can drop NaN dates or fill them if needed. To drop days with NaN (e.g., non-trading days), you can do `price_df.dropna(how='all', inplace=True)` (drops rows where *all* values are NaN). This will remove weekends/holidays since none of the stocks traded then. Alternatively, to fill missing days forward or backward use methods like `price_df.fillna(method='ffill')` (forward-fill), but in stock prices it's common to just omit non-trading days or keep them as gaps.  
#    d. **Set Date Index (if not already)**: If you haven't already, ensure that the 'Date' is the index of `price_df` and that it's a DatetimeIndex (it should be, from our earlier conversion). You can verify `price_df.index.dtype` or use `price_df.index = pd.to_datetime(price_df.index)` if needed (though it should already be datetime from our combined data).

# **6. Time Series Analysis**
#    a. **Daily Returns**: Calculate daily percentage returns for each stock. Now that you have `price_df` with each column as a stock's closing price, you can use the pandas `.pct_change()` function on this DataFrame to get returns. For example: `returns_df = price_df.pct_change()`. The first day will have NaN return (since there's no previous day to compare). You may multiply by 100 if you prefer percentage format. You can also drop the first NaN or fill it with 0 for convenience.  
#    b. **Summary of Returns**: Inspect `returns_df.describe()` to see mean daily return, std dev, etc., for each stock. Which stock had the highest average daily return in this period? Which was most volatile (highest std dev of returns)? Note: daily mean returns will be very small numbers (fractions of a percent).  
#    c. **Correlation of Returns**: Compute the correlation matrix of daily returns to see how the stocks move relative to each other. Use `returns_df.corr()`. This will produce a matrix (DataFrame) where the entry [i,j] is the correlation between stock i's and stock j's daily returns. A value close to 1 means they move very similarly, 0 means no linear correlation, and negative means they often move opposite. Print the correlation matrix. Identify which two stocks in your selection are the most correlated, and which are the least.  
#    d. **Resampling - Monthly Averages**: Using the `price_df` (daily prices), resample the data to a coarser frequency to see longer-term trends. For instance, calculate the **monthly average closing price** for each stock. Use `price_df.resample('M').mean()`. This groups the data by month (based on Date index) and computes the mean close in each month. You could also compute monthly open or volume similarly if needed. Store this in `monthly_avg_df` and inspect it (e.g., `monthly_avg_df.head()`). The index will be end-of-month dates by default.  
#    e. **Identifying Trends**: With monthly data or daily data, you can also identify trends. For example, find which month had the highest average price for each stock, or which month had the biggest gain. For the former, you could take `monthly_avg_df.idxmax()` to get the month (index) where each stock's average price was highest. (Ensure to interpret the results; idxmax returns a Timestamp likely at end-of-month.)  
#    f. **Rolling Window Calculations**: Compute rolling statistics to analyze trends and volatility. For example, calculate a 20-day moving average of the closing price for each stock. Use `price_df.rolling(window=20).mean()`. This will produce a DataFrame of the same shape with each value being the average of the past 20 days for that stock. You might add this as new columns or handle it separately. Also, you can compute a 20-day moving standard deviation (volatility) with `.rolling(window=20).std()`. These rolling metrics smooth out short-term fluctuations and highlight longer trends.  
#    g. **Add Rolling to DataFrame** (optional): If you want to compare the moving average with actual prices, you might add it as additional columns. For instance, you could add columns to `price_df` like `AAPL_MA20` = 20-day MA of AAPL, etc. But an easier way for visualization is just to compute on the fly when plotting.

# **7. Visualization**
#    a. **Plot Closing Prices**: Using Matplotlib (or Pandas' built-in plotting), create a line plot of the daily closing prices of each stock over time on the same chart. This will allow you to visualize how each stock performed relative to the others over the period. Use different colors/labels for each stock. For example:  
#       ```python
#       plt.figure(figsize=(10,6))
#       for ticker in tickers:
#           plt.plot(price_df.index, price_df[ticker], label=ticker)
#       plt.title('Daily Closing Prices')
#       plt.xlabel('Date')
#       plt.ylabel('Price (USD)')
#       plt.legend()
#       plt.show()
#       ```  
#       This will plot each ticker's price. Observe the trends: did one stock outperform others? Were there any big spikes or drops?  
#    b. **Plot Moving Average**: Pick one stock and plot its closing price along with its 20-day moving average to illustrate the trend. For example,  
#       ```python
#       plt.figure(figsize=(8,4))
#       plt.plot(price_df.index, price_df['AAPL'], label='AAPL Close', color='blue')
#       plt.plot(price_df.index, price_df['AAPL'].rolling(20).mean(), label='AAPL 20-day MA', color='orange')
#       plt.title('AAPL Price vs 20-day Moving Average')
#       plt.xlabel('Date'); plt.ylabel('Price (USD)')
#       plt.legend(); plt.show()
#       ```  
#       You can create similar plots for other stocks or different rolling windows. This shows how the moving average smooths out short-term fluctuations.  
#    c. **Plot Daily Returns Distribution** (optional): For a different insight, you might plot a histogram of daily returns for each stock to visualize its volatility distribution. You could use `plt.hist(returns_df['AAPL'], bins=50)` for example, or use Pandas `returns_df['AAPL'].plot.hist()`. Compare the spread of returns for each stock. This requires some familiarity with histograms and is optional.  
#    d. **Additional Visuals**: Feel free to add any other plots that help illustrate your analysis (volume over time, scatter plot of one stock's returns vs another's, etc.). Visualizations can provide intuitive insight beyond the raw numbers.

# **8. Save Results (Optional)**
#    a. After analysis, you can save your combined or processed DataFrames to files for future reference or for others to examine. For instance, save the final wide-format price data or the combined DataFrame to a CSV file using `DataFrame.to_csv('filename.csv')`. For example: `price_df.to_csv('stock_closing_prices.csv')` will save the daily closing prices for all your tickers. You could also save the combined long dataframe with all data to a file. (In Codespaces, the file will appear in the directory and you can download it if needed.)  
#    b. Ensure not to save sensitive information (like the API key) in any shared file. It's okay in your code, but avoid logging it or printing it in output.

# **9. Interpretation and Conclusions** 
#    (No code needed here, but in a report you'd discuss these) 
#    - Look at the results of your analysis and write down a summary. Which stock had the best performance over the period? (You could evaluate by total return from start to end.) Which was most volatile? How correlated were the stocks? Were there any particular months where all stocks fell or rose (check the monthly data)? How do the moving averages inform about trends? 
#    - These interpretations help solidify the insights gained from the data. Make sure you understand what each analysis step indicates about the stock behavior.

# Now that we've outlined the steps, let's implement the solution. The code below follows the instructions above. 
# (Note: Running this code will actually fetch data from the API, which requires internet access and uses the provided API key. 
# Ensure your environment has access and the API key is valid. Limit your ticker choices to a few to avoid rate limits.)


























# Solution Implementation:

# Step 1: Setup
import pandas as pd
import requests
import matplotlib.pyplot as plt

API_KEY = "dIUMbUHa3jguPZ9WiF5HUgIS4FWhPWlq"  # Provided Polygon API Key
tickers = ["AAPL", "MSFT", "GOOGL"]         # Choose your stock tickers
start_date = "2022-01-01"                   # Start of data range (inclusive)
end_date   = "2023-01-01"                   # End of data range (exclusive or inclusive depending on API; polygon treats end as inclusive)

# Prepare a dictionary to hold data frames for each ticker
data_frames = {}

for ticker in tickers:
    # Construct the request URL for the Polygon aggregates API
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=5000&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {ticker}. HTTP Status: {response.status_code}")
        continue
    data = response.json()
    # Check if the response contains results
    if 'results' not in data or data['results'] is None:
        print(f"No data returned for {ticker}. Response: {data}")
        continue
    # Create DataFrame from results list
    df = pd.DataFrame(data['results'])
    if df.empty:
        print(f"No data for {ticker} in the given date range.")
        continue
    # Convert timestamp to datetime and rename it to 'Date'
    df['Date'] = pd.to_datetime(df['t'], unit='ms')
    # Rename columns for clarity
    df.rename(columns={'o':'Open','h':'High','l':'Low','c':'Close','v':'Volume','t':'Timestamp'}, inplace=True)
    # We can drop the original 'Timestamp' (millisecond timestamp) column and any others not needed (like 'n' or 'vw' if present)
    drop_cols = [col for col in ['Timestamp','n','vw'] if col in df.columns]
    if drop_cols:
        df.drop(columns=drop_cols, inplace=True)
    # Add a 'Ticker' column
    df['Ticker'] = ticker
    # (Optional) Sort by Date just in case (should already be sorted due to sort=asc in API call)
    df.sort_values(by='Date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    # Store DataFrame in dictionary
    data_frames[ticker] = df
    # Print sample of data
    print(f"\nData for {ticker}: {len(df)} rows")
    print(df.head(3))

# Combine all ticker data into one DataFrame
combined_df = pd.concat(list(data_frames.values()), ignore_index=True)
print(f"\nCombined DataFrame shape: {combined_df.shape}")  # rows x cols
print(combined_df.head(5))

# Ensure combined data is sorted by Date (and Ticker as secondary for consistency)
combined_df.sort_values(by=["Date","Ticker"], inplace=True)
combined_df.reset_index(drop=True, inplace=True)

# Step 4: Exploratory Data Analysis (EDA)

# Basic descriptive statistics for closing prices by ticker
print("\nDescriptive stats for Closing Prices by Ticker:")
print(combined_df.groupby('Ticker')['Close'].describe())

# Total and average volume by ticker
total_volume = combined_df.groupby('Ticker')['Volume'].sum()
avg_volume = combined_df.groupby('Ticker')['Volume'].mean()
print("\nTotal Volume traded in period by Ticker:")
print(total_volume)
print("\nAverage Daily Volume by Ticker:")
print(avg_volume)

# Add daily absolute change and percent change columns
combined_df['DailyChange'] = combined_df['Close'] - combined_df['Open']
combined_df['DailyPctChange'] = (combined_df['Close'] - combined_df['Open']) / combined_df['Open'] * 100

# UpDay column: True if Close > Open
combined_df['UpDay'] = combined_df['Close'] > combined_df['Open']
# Proportion of Up days per ticker
up_day_ratio = combined_df.groupby('Ticker')['UpDay'].mean() * 100  # in percentage
print("\nPercentage of days that were UpDays for each Ticker:")
print(up_day_ratio)

# Highest and lowest closing price for each ticker (and the dates on which they occurred)
print("\nMax and Min closing prices for each Ticker (and corresponding dates):")
for tic in tickers:
    df_tic = combined_df[combined_df['Ticker'] == tic]
    max_close = df_tic['Close'].max()
    max_date = df_tic.loc[df_tic['Close'].idxmax(), 'Date']
    min_close = df_tic['Close'].min()
    min_date = df_tic.loc[df_tic['Close'].idxmin(), 'Date']
    print(f"{tic}: Highest Close = {max_close:.2f} on {max_date.date()}, Lowest Close = {min_close:.2f} on {min_date.date()}")

# Step 5: Pivot to get wide format (Date as index, tickers as columns for Close)
price_df = combined_df.pivot(index='Date', columns='Ticker', values='Close')
# Sort index (dates) just to be sure
price_df.sort_index(inplace=True)

# Drop rows (dates) where all values are NaN (non-trading days if any)
price_df.dropna(how='all', inplace=True)

print(f"\nPivoted price DataFrame (head):")
print(price_df.head(5))

# Step 6: Time Series Analysis

# Daily returns for each stock
returns_df = price_df.pct_change() * 100  # multiply by 100 to express in percentage
# (First row for each stock will be NaN because of no previous day to compare.)
returns_df.dropna(how='all', inplace=True)  # drop the first day (NaNs in all cols)
print("\nDaily Returns (% change) descriptive stats:")
print(returns_df.describe())  # show stats like mean, std for returns

# Correlation of daily returns
corr_matrix = returns_df.corr()
print("\nCorrelation matrix of daily returns:")
print(corr_matrix)

# Resample to monthly frequency for average closing price
monthly_avg_df = price_df.resample('M').mean()
print("\nMonthly average closing prices (first 5 rows):")
print(monthly_avg_df.head(5))

# Identify month of highest average price for each stock
max_month = monthly_avg_df.idxmax()
print("\nMonth of highest average closing price for each stock:")
for tic in tickers:
    if pd.notna(max_month[tic]):
        print(f"{tic}: {max_month[tic].strftime('%Y-%m')} (Avg Close = {monthly_avg_df.loc[max_month[tic], tic]:.2f})")

# Compute 20-day moving average for each stock's close
ma20_df = price_df.rolling(window=20).mean()

# Step 7: Visualization

# Plot daily closing prices for each stock
plt.figure(figsize=(10,6))
for tic in tickers:
    plt.plot(price_df.index, price_df[tic], label=tic)
plt.title('Daily Closing Prices')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Plot one stock's price vs 20-day moving average (using AAPL as example)
plt.figure(figsize=(8,4))
plt.plot(price_df.index, price_df['AAPL'], label='AAPL Close', color='blue')
plt.plot(price_df.index, ma20_df['AAPL'], label='AAPL 20-day MA', color='orange')
plt.title('AAPL: Close Price vs 20-day Moving Average')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# (Optional) Plot histogram of daily returns for each stock for distribution comparison
plt.figure(figsize=(8,5))
for tic in tickers:
    plt.hist(returns_df[tic].dropna(), bins=50, alpha=0.5, label=tic)
plt.title('Distribution of Daily Returns')
plt.xlabel('Daily Return (%)')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# Step 8: Save results to CSV (for example, save the wide price data)
price_df.to_csv("stock_closing_prices.csv")
print("\nSaved wide format closing prices to 'stock_closing_prices.csv'")
