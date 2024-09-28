from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px

# Define your connection string
engine = create_engine('postgresql+psycopg2://emadee:password@localhost:5432/test_db')

# Define SQL query to fetch stock data
query = """
    SELECT record_date, close_value, ticker
    FROM stocks
    WHERE ticker = 'A' 
    AND record_date BETWEEN '2024-04-01' AND '2024-5-31'
"""

# Read data into a pandas DataFrame
df = pd.read_sql(query, engine)

# Convert record_date to datetime
df['record_date'] = pd.to_datetime(df['record_date'])
# Plot a line chart for the closing values of the stock
fig = px.line(df, x='record_date', y='close_value', title='Stock Closing Prices Over Time')

# Show the plot
fig.show()