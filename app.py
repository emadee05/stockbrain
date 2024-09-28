import flask
from flask import request, jsonify, render_template
import sqlite3
import getpass as gp
import pandas as pd
from sqlalchemy import create_engine, text
import plotly
import google.generativeai as genai
from load_creds import load_creds, load_iam_creds
import numpy as np 
import os 


# Configure generative AI with credentials
creds = load_iam_creds()
genai.configure(credentials=creds)
print()
print('Available base models:', [m.name for m in genai.list_models()])
print()
print('Available tuned models:')
try:
    tuned_models = genai.list_tuned_models()
    for i, model in enumerate(tuned_models):
        print(model.name)
        if i >= 4:  # Limit to first 5 models
            break
except Exception as e:
    print(f"Error listing tuned models: {e}")


app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Model configuration
model_name = 'gemini-1.5-flash'
model = genai.GenerativeModel(model_name=f'models/{model_name}')

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to FundPage</h1>
<p>A prototype API for reading the data from the server.</p>'''


@app.route('/ui', methods=['GET', 'POST'])
def api_filter():
    if request.method == 'POST':
        tk = request.form.get('tk', 'MSFT')
        stdate = request.form.get('stdate', '2019-01-01')
        eddate = request.form.get('eddate', '2021-05-01')


        servername='127.0.0.1'
        engine = create_engine(f'postgresql+psycopg2://emadee:password@{servername}:5432/test_db')
        query = text(f"""
            SELECT record_date, close_value, ticker
            FROM stocks
            WHERE ticker = '{tk}' 
            AND record_date BETWEEN '{stdate}' AND '{eddate}'
        """)
        df = pd.read_sql(query, engine, params={"tk": tk, "stdate": stdate, "eddate": eddate})
        # Convert the DataFrame to a list of dictionaries (for rendering in HTML)

        print("DataFrame from SQL Query:")
        print(df)


        stock_data = df.to_dict(orient='records')


        print("Stock Data (List of Dictionaries):")
        print(stock_data)
        summary = generate_summary(stock_data)

        print("generated summary")
        print(summary)
        explanation = get_explanation(summary)
        # Render the template with the stock data
        return render_template('form.html', stock_data=stock_data, explanation=explanation)
    return render_template('form.html')



def get_explanation(summary):
    prompt = f"Here are some significant rises and drops in the stock data:\n{summary}\nPlease explain why these rises and drops might have occurred."
    result = model.generate_content(prompt)
    # # client = openai.OpenAsI()
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",  # or "gpt-3.5-turbo"
    #     messages=[
    #         {"role": "system", "content": "You are an expert financial analyst, teaching a highschooler with little financial knowledge or news awareness."},
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    # return response.choices[0].message
    print("this is the result alalalla :")
    print(result)
    return result.text
    # return jsonify({'response': result.text}) 
# 404 Error handling
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run(host="0.0.0.0", port=5001)
