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

def get_stock(ticker,startdate,enddate):
    url=f'https://finance.yahoo.com/quote/{ticker}/history?period1={startdate}&period2={enddate}'
    print(url)
    soup = get_soup(url)
    thead = soup.find('main').find('article')
    cells=thead.find('tr')
    columnname=[cell.text.split(' ')[0] for cell in cells]
    table = soup.find('tbody')
    rows=table.find_all('tr')
    all_data = []
    for row in rows:
        cells=row.find_all('td')
        data = [cell.text for cell in cells]
        print(data)
        all_data.append(data)
    df = pd.DataFrame(all_data[1:],columns=columnname)
    #df = None
    return df
def get_company(ticker):
    url=f'https://finance.yahoo.com/quote/{ticker}/financials'
    soup = get_soup(url)
    s_main=soup.find("main")
    compinfo = s_main.h1
    print(compinfo)
    str=compinfo.text
    company=str[0:str.rfind("(")].strip()
    symbol=str[str.rfind("(")+1:str.rfind(")")]
    return (company,symbol)

def get_finance(ticker):
    url=f'https://finance.yahoo.com/quote/{ticker}/financials'
    soup = get_soup(url)
    main_article = soup.find('article').find('article')
    section = main_article.find('section')
    table= section.find('div').find('div')
    #print(table)
    all_data = []
    row = table.contents[2] 
   

    for content in table.contents:
        if content:
            content_sub = content
            print(len(content))
            if len(content) ==1:
                data = [cell for cell in content_sub.stripped_strings]
                if len(data)>1:
                    print("###",data)
                    all_data.append(data)
            else:
                sub_contents =content.children
                for rows in sub_contents:
                    data = [cell for cell in rows.stripped_strings]
                    if len(data)>1:
                        all_data.append(data)


    df = pd.DataFrame(all_data[1:],columns=all_data[0])
    
    return df
    

 


ticker = 'AMZN'
format='%Y-%m-%d %H:%M:%S'
startdate='2018-01-01 19:00:00'
startdate=int(datetime.strptime(startdate, format).timestamp())
dt= '2018-06-01 19:00:00'
enddate = int(datetime.strptime(dt, format).timestamp())
df_stocks = get_stock(ticker,startdate,enddate)
print(df_stocks.head)

par=get_finance(ticker)
print(par)