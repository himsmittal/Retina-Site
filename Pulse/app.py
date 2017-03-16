from flask import Flask, render_template, request
import requests
import json
from datetime import datetime


app = Flask(__name__)

pio_api = "http://10.204.156.100:8000/queries.json"

DATA_POINTS = 900

@app.route('/')
def home():
    """
    Home Page
    """
    return render_template('index.html')


@app.route('/plot')
def anomaly_detection():
    """
    Anomaly Detection Graphing
    """
    datasource, dataset = request.args.get('datasource'), request.args.get('dataset')
    if datasource and dataset:
        data_dict = {"q" : []}
        value_list = []
        with open('data/db_host_cpu_usage.csv', 'r') as f:
            for line in f.readlines():
                data_dict['q'].append(line.split(",")[1].strip())
                value_list.append(map(float, line.strip().split(",")))
        """
        headers = {'content-type' : 'application/json'}
        response = requests.post(pio_api, data=json.dumps(data_dict), headers=headers)
        if response.status_code == 200:
            response_dict = json.loads(response.content)
        """
        with open('data/cpu_anomalies.json', 'r') as f:
            response_dict = json.loads(f.read())
            anomaly_list = []
            for timestamp, anomaly in zip(value_list, response_dict['p']):
                anomaly_list.append([timestamp[0], anomaly])
        return render_template('plot.html', status="success", values=value_list[:DATA_POINTS], anomalies=anomaly_list[:DATA_POINTS])
    else:
        return render_template('plot.html', status="fail")


@app.route('/team')
def team():
    """
    Team page
    """
    return render_template('team.html')


@app.route('/predictions')
def prediction():
    """
    Predictions Graphing
    """
    datasource, dataset = request.args.get('datasource'), request.args.get('dataset')
    if datasource and dataset:
        value_list = []
        prediction_list = []
        with open('data/cp_power_supply_datacenter.csv', 'r') as f:
            for line in f.readlines():
                fields = line.split(",")
                value_list.append(map(float, [fields[0], fields[1]]))
                prediction_list.append(map(float, [fields[0], fields[2]]))
        return render_template('prediction.html', status="success", values=value_list[:DATA_POINTS], predictions=prediction_list[:DATA_POINTS])
    else:
        return render_template('prediction.html', status="failed", error="Request Failed")
    return render_template('prediction.html')


@app.route('/notify', methods=['POST'])
def notify():
    title, description = (request.form['title'], request.form['description'] + "\nPossible related causes : Request per second\nPlease ignore request. Testing API")
    return ""



@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
