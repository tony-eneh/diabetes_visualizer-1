# Diabetes Data Visualizer

## Project Overview
The **Diabetes Data Visualizer** is a Flask-based web application that enables users to upload their blood sugar data in CSV format and get valuable insights, visualizations, and trend analyses. The application calculates average blood sugar levels, identifies peaks, and provides recommendations based on user data.

## Features
- **Upload CSV Data**: Upload blood sugar readings in CSV format with `Date` and `BloodSugar` columns.
- **Data Insights**: Displays average and peak blood sugar levels, morning vs. evening trends.
- **Interactive Visualizations**: Visualize blood sugar data using Plotly.js, offering zoom, pan, and hover features.
- **Trend Analysis**: Detect trends using a simple moving average (SMA) and identify critical patterns.
- **Flexible Date Parsing**: Supports multiple date formats (`MM/DD/YYYY`, `YYYY-MM-DD`, etc.) for flexible data input.

## Technologies Used
- **Backend**: Python, Flask
- **Frontend**: HTML, JavaScript (Plotly.js)
- **Data Processing**: Pandas, Numpy
- **CSV Parsing**: Pandas

---

## Installation

### Prerequisites
- **Python 3.x** installed.
- **pip** package manager.

### Clone the Repository
```bash
git clone https://github.com/Preciousejiba/diabetes-data-visualizer.git
cd diabetes-data-visualizer

### Create a Virtual Environment (Optional)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

### Install Dependencies
```bash
pip install -r requirements.txt

### Run the Application
```bash
python app.py






