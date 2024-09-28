import psycopg2 
import mystock_webscraper
import pandas as pd 
from datetime import datetime
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://emadee:password@localhost:5432/test_db')

# connection = psycopg2.connect(database = 'test_db', user='emadee', password='password', host='localhost', port='5432')

# cursor = connection.cursor()
# query= 'select * from stock_data'
# cursor.execute(query)

# version = cursor.fetchall()
# print(f"Connected to PostgreSQL - version: {version}")

df = pd.read_csv('nasdeqlist.csv')

symbols = df['Symbol']
names = df['Name']
first_tickers = symbols[:10]
first_names = names[:10]

necessary_columns = ['Date','Open', 'High', 'Low', 'Close', 'Adj', 'Volume']
newcolumns = ['record_date','open_value','high_value','low_value','close_value','adj_value','volume','ticker','name']

datas = []

for ticker, name in zip(first_tickers, first_names): 
    format='%Y-%m-%d %H:%M:%S'
    startdate='2024-01-01 19:00:00'
    startdate=int(datetime.strptime(startdate, format).timestamp())
    enddate = '2024-06-01 19:00:00'
    enddate = int(datetime.strptime(enddate, format).timestamp())
    df_stocks = mystock_webscraper.get_stock_data(ticker, startdate, enddate)
  
    # Ensure the necessary columns exist in the DataFrame
    #if all(col in df_stocks.columns for col in necessary_columns):
    if not df_stocks.empty:
        # # Drop rows where key columns are NaN
        # df_cleaned = df.dropna(subset=necessary_columns)
        df_stocks['ticker'] = ticker
        df_stocks['name'] = name
        # # Print the DataFrame columns for debugging
        # print(df_cleaned.columns)
        df_stocks.columns = newcolumns
        # print(df_stocks)

        # # for col in ['open_value', 'high_value', 'low_value', 'close_value', 'adj_value', 'volume']:
        # #     df_stocks[col] = pd.to_numeric(df_stocks[col], errors='coerce')
        # # df_stocks.dropna(subset=['open_value', 'high_value', 'low_value', 'close_value', 'adj_value', 'volume'], inplace=True)
        # print(df_stocks)
        datas.append(df_stocks)

        # Write the cleaned DataFrame to PostgreSQL if it's not empty
        # if not df_cleaned.empty:
        
   
    else:
        print(f"Data for ticker {ticker} is missing necessary columns.")

print(datas)
# Combine all DataFrames into one
if datas:
    final_df = pd.concat(datas, ignore_index=True)
    
    # Write the entire data at once to SQL
    final_df.to_sql('stocks', engine, if_exists='append', index=False)
else:
    print("No valid data to write to the database.")

# try:
#             df_stocks.to_dict('new_dict')
# except: 
#             pass

# to_sql('stocks', engine, if_ exists='append', index=False)
