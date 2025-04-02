from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import os
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page


@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and processing


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        data = pd.read_csv(filepath)

        # Process the data for analysis
        avg_blood_sugar, peak_blood_sugar, trends, insights, recommendations = process_data(
            data)

        return render_template('result.html',
                               avg_blood_sugar=avg_blood_sugar,
                               peak_blood_sugar=peak_blood_sugar,
                               trends=trends,
                               insights=insights,
                               recommendations=recommendations,
                               data=data.to_json(orient="records"))  # Send data to the template

# Process data: analyze CSV and generate insights


def process_data(data):
    # Assuming CSV has columns 'Date' and 'BloodSugar'
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values('Date', inplace=True)

    avg_blood_sugar = data['BloodSugar'].mean()
    peak_blood_sugar = data['BloodSugar'].max()

    # Trend Analysis (Simple moving average to detect upward/downward trends)
    data['SMA'] = data['BloodSugar'].rolling(
        window=5).mean()  # 5-day moving average
    data['Trend'] = np.where(
        data['SMA'] > data['BloodSugar'], 'Decreasing', 'Increasing')

    trends = "Increasing" if (
        data['SMA'].iloc[-1] > data['SMA'].iloc[0]) else "Decreasing"

    # Insights and recommendations based on average and trends
    insights = ""
    recommendations = ""

    if avg_blood_sugar > 180:
        insights = "Your average blood sugar is quite high."
        recommendations = "Consider reducing carb intake, and consult a healthcare professional."
    elif avg_blood_sugar < 70:
        insights = "Your blood sugar levels are consistently low."
        recommendations = "Ensure regular meals and discuss with a doctor if necessary."
    else:
        insights = "Your blood sugar levels are within a normal range."
        recommendations = "Continue maintaining your diet and regular exercise."

    if trends == "Increasing":
        insights += " There is an upward trend in your blood sugar levels."
        recommendations += " Keep an eye on the upward trend and consult your doctor if it persists."
    else:
        insights += " There is a downward trend in your blood sugar levels."
        recommendations += " Ensure you're not overcorrecting if blood sugar levels continue to decrease."

    return avg_blood_sugar, peak_blood_sugar, trends, insights, recommendations


if __name__ == '__main__':
    app.run(debug=True, port=80)
