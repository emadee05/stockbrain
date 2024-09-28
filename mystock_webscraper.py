import pandas as pd
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup


url='https://finance.yahoo.com/quote/{ticker}/history?period1={startdate}&period2={enddate}'

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'}

def get_soup(url):
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.content, 'html.parser')

def get_stock_data(ticker, startdate, enddate):
    url=f'https://finance.yahoo.com/quote/{ticker}/history?period1={startdate}&period2={enddate}'
    soup=get_soup(url)
    head = soup.find('main').find('article')
    tr_cells = head.find('tr')
    column_names=[cell.text.split(' ')[0] for cell in tr_cells]
    table=soup.find('tbody')
    table_data = []
    for row in table:
        cells=row.find_all('td')
        if len(cells)==7:
            data=[cell.text for cell in cells]
            table_data.append(data)
    df = pd.DataFrame(table_data[1:],columns=column_names)
    return df

def get_company(ticker):
    url=f'https://finance.yahoo.com/quote/{ticker}/financials'
    soup = get_soup(url)
    s_main=soup.find("main")
    company_info = s_main.h1
    company_name = company_info[0:str.find("()")].strip()
    company_symbol = company_info[str.rfind("(")+1:str.rfind(")")]
    return (company_name, company_symbol)

ticker = 'AAGRW'
format='%Y-%m-%d %H:%M:%S'
startdate='2024-03-30 19:00:00'
startdate=int(datetime.strptime(startdate, format).timestamp())
dt= '2024-06-01 19:00:00'
enddate = int(datetime.strptime(dt, format).timestamp())

df = get_stock_data(ticker, startdate, enddate)
if df.empty:
    print("empty")
print(df)

