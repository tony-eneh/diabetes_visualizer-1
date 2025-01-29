from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file")
    if not file.filename.endswith('.csv'):
        return render_template('index.html', error="Only CSV files are allowed")

    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        data = pd.read_csv(filepath)

        # Process the data
        avg_blood_sugar, peak_blood_sugar, trend, insights = process_data(data)

        # Generate the plot
        plot_json = generate_plots(data)
        
        return render_template('result.html',
                               avg_blood_sugar=avg_blood_sugar,
                               peak_blood_sugar=peak_blood_sugar,
                               trend=trend,
                               insights=insights,
                               plot_json=plot_json)
    except Exception as e:
        return render_template('index.html', error=f"Error processing file: {e}")

def process_data(data):
    # Validate and clean the data
    data.columns = data.columns.str.strip()
    if 'Date' not in data.columns or 'BloodSugar' not in data.columns:
        raise KeyError("The CSV file must contain 'Date' and 'BloodSugar' columns.")
    
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data = data.dropna(subset=['Date', 'BloodSugar'])
    data.sort_values('Date', inplace=True)

    # Calculate statistics
    avg_blood_sugar = data['BloodSugar'].mean()
    peak_blood_sugar = data['BloodSugar'].max()

    # Determine trend
    trend = "Increasing" if data['BloodSugar'].iloc[-1] > data['BloodSugar'].iloc[0] else "Decreasing"

    # Generate insights
    insights = []
    if avg_blood_sugar < 70:
        insights.append("Your average blood sugar level is too low (Hypoglycemia).")
    elif avg_blood_sugar <= 140:
        insights.append("Your average blood sugar level is within the normal range.")
    elif avg_blood_sugar <= 199:
        insights.append("Your average blood sugar level indicates pre-diabetes. Monitor closely.")
    else:
        insights.append("Your average blood sugar level indicates diabetes. Consult a healthcare provider.")

    return avg_blood_sugar, peak_blood_sugar, trend, insights

def generate_plots(data):
    trace1 = go.Scatter(x=data['Date'], y=data['BloodSugar'], mode='lines+markers', name='Blood Sugar')
    layout = go.Layout(
        title='Blood Sugar Levels Over Time',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Blood Sugar Levels')
    )
    fig = go.Figure(data=[trace1], layout=layout)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == '__main__':
    app.run(debug=True)
