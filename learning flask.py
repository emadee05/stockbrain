import flask
from flask import request, jsonify
import sqlite3
import getpass as gp
import pandas as pd
from sqlalchemy import create_engine, text
import plotly

import numpy as np 

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to FundPage</h1>
<p>A prototype API for reading the data from the server.</p>'''


@app.route('/api/all', methods=['GET'])
def api_all():
    servername='192.168.1.51'
    engine = create_engine(f'postgresql+psycopg2://emadee:password@{servername}:5432/test_db')

    query = text("""
        SELECT record_date, close_value, ticker
        FROM stocks
        WHERE ticker = 'A' 
        AND record_date BETWEEN '2024-04-01' AND '2024-5-31'
    """)    
    df = pd.read_sql(query, engine)
    results=df.to_json(orient='records') 
    return results
  



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/', methods=['GET'])
def api_filter():
    if 'ftype' in request.args:
        ftype=request.args['ftype']
    else:
        ftype='Stock'
    if 'tk' in request.args:
        tk=request.args['tk']
    else:
        tk='MSFT'
    if 'stdate' in request.args:
        stdate=request.args['stdate']
    else:
        stdate='2019-1-1'
    if 'eddate' in request.args:
        eddate=request.args['eddate']
    else:
        eddate='2021-5-1'      


    servername='192.168.1.51'
    engine = create_engine(f'postgresql+psycopg2://emadee:password@{servername}:5432/test_db')
    query = text(f"""
        SELECT record_date, close_value, ticker
        FROM stocks
        WHERE ticker = '{tk}' 
        AND record_date BETWEEN '{stdate}' AND '{eddate}'
    """)
    df = pd.read_sql(query, engine)
    results=df.to_json(orient='records') 
    return results

app.run()