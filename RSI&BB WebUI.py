import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output
from datetime import date, timedelta
from numpy import datetime64, dtype
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objs as pgo

from pandas import json_normalize

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        html.Div([html.Img(src=app.get_asset_url('FundPage.PNG'))],
        style={"width": "80%",'margin':25, 'textAlign': 'center'}
        ),
        html.Div([
            html.Label('Fund Type'),           
            dcc.RadioItems(id='FundType',
                options=[
                {'label': 'Fund', 'value': 'Fund'},
                {'label': 'Index', 'value': 'Index'},
                {'label': 'Stock', 'value': 'Stock'}
            ],
                value='Stock',
                labelStyle={'display': 'inline-block'}
            ),            

        #], style={"width": "50%",'margin':25, 'textAlign': 'left'}, 
        #),
        #html.Div([    
            html.Label('Fund Name'),
            dcc.Input(
                id="Fname", type="text",
                debounce=True, placeholder="MSFT",
            ),
            html.Label('Starting / Ending Date'),
            dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2022, 1, 1),
            initial_visible_month=date(2018, 1, 1),
            display_format='Y-M-D',
            with_portal=True,
            start_date_placeholder_text="Start Period",
            end_date_placeholder_text="End Period",
            end_date=date.today()            
            ),

            
        ],
        style={"width": "60%",'columnCount': 3,'margin':10, 'textAlign': 'left'},
        
        ), 
        #html.Hr(),
        html.Div(id="number-out",style={"width": "60%",'margin':25, 'textAlign': 'left'}),
        html.Div([
        dcc.Graph(
            id='BB-lines',
            hoverData={'points': [{'customdata': 'Value'}]}
            ),
               
        dcc.Graph(
            id='RSI-lines',
            hoverData={'points': [{'customdata': 'Value'}]}
            )
        ], style={'width': '80%', 'display': 'inline-block', 'padding': '0 10'}),
    ]
   
     
)


@app.callback(
    Output("BB-lines", "figure"),
    Output("RSI-lines", "figure"),
    Output("number-out", "children"),
    Input("FundType", "value"),
    Input("Fname", "value"),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')],
)

def update_output(fval,tval,start_date, end_date):
    string_prefix = 'Fund Type: '+str(fval) +' Ticker: '+str(tval)
    if fval is None:
        fval='Stock'
    if tval is None:
        tval='MSFT'
    if start_date is None:        
        start_date=date.today()-timedelta(days=365)
       
    if end_date is None:
        end_date=date.today()
    ftype=str(fval)
    tk=str(tval)
    url="http://127.0.0.1:5000/api/?ftype={}&tk={}&stdate={}&eddate={}".format(fval,tval,start_date,end_date)

    datarequest=requests.get(url)
    data=datarequest.json()
    re=json_normalize(data)
    re['Date']=re['Date'].astype(datetime64)
    re['Date']=re['Date'].dt.date
    re['BOLU']=re['BOLU'].astype(float)
    re['BOLD']=re['BOLD'].astype(float)
    fig=px.line(re,x='Date',y=['Price','BOLD','BOLU'])
    mess= " Company:{},    Start: {}, End: {}".format(re['Fund name'][1], start_date,end_date)
    fig2=px.line(re,x='Date',y=['RSI'])
    fig2.update_traces(line_color='gold')
    fig2.add_hline(y=70,line_dash='dot', annotation_text=' 70%')
    #fig2.update_traces(line_color='pink')
    fig2.add_hline(y=30,line_dash='dot', fillcolor="red", annotation_text=' 30%')
    fig2.update_yaxes(range=[0,100])
    fig.update_layout(plot_bgcolor="#f1f2ee")
    fig2.update_layout(plot_bgcolor="#f1f2ee")
    return fig,fig2,mess


if __name__ == "__main__":
    app.run_server(debug=True)