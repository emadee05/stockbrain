import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


# Connect to PostgreSQL
engine = create_engine('postgresql+psycopg2://emadee:password@localhost:5432/test_db')

# Define the ticker, start, and end dates
ticker = 'A'
start_date = '2024-01-01'
end_date = '2024-06-01'

# Write the SQL query
query = f"""
SELECT record_date, close_value 
FROM stocks 
WHERE ticker = '{ticker}' 
AND record_date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY record_date;
"""

# Execute the query and load the data into a Pandas DataFrame
df = pd.read_sql(query, engine)

# Display the DataFrame
print(df)

df['record_date'] = pd.to_datetime(df['record_date'])

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df['record_date'], df['close_value'], marker='o', linestyle='-', color='b')

# Customize the plot
plt.title(f"Stock Close Values for {ticker} from {start_date} to {end_date}")
plt.xlabel("Date")
plt.ylabel("Close Value")
plt.grid(True)

# Show the plot
plt.show()