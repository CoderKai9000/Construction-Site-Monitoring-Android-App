from flask import Flask, render_template, jsonify, request
import json
import time
from datetime import datetime
import os

app = Flask(__name__)

# Global variable for interval time (in seconds)
interval = 5  # Default interval to 5 seconds
last_sent_time = None  # To store the last sent time

# Clear log file when the app starts
@app.before_first_request
def clear_log():
    if os.path.exists("log.txt"):
        with open("log.txt", "w") as file:
            file.truncate(0)  # Clear the contents of the file


@app.route('/')
def index():
    return render_template('log.html')


@app.route('/log_data', methods=['POST'])
def log_data():
    global last_sent_time
    current_time = time.time()
    if last_sent_time is None or current_time - last_sent_time >= 5:
        data = request.get_json()
        
        person_count = sum(1 for item in data if item["label"] == "person")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("log.txt", "a") as file:
            file.write(f"{timestamp} - {person_count}\n")
        last_sent_time = current_time
        return jsonify({"message": "Data logged successfully", "person_count": person_count})
    else:
        return jsonify({"message": "Not enough time has passed since the last upload"}), 200



@app.route('/get_graph')
def get_graph():
    timestamps = []
    person_counts = []

    try:
        with open("log.txt", "r") as file:
            for line in file:
                parts = line.split(" - ")
                timestamps.append(parts[0])
                person_counts.append(int(parts[1]))
    except FileNotFoundError:
        return jsonify({"error": "log.txt not found"}), 404

    if not timestamps or not person_counts:
        return jsonify({"error": "No data available for graph"}), 400
    
    return jsonify({
        "timestamps": timestamps,
        "person_counts": person_counts
    })



@app.route('/set_interval', methods=['POST'])
def set_interval():
    global interval
    try:
        # Get the new interval from the request
        new_interval = int(request.form.get("interval"))
        
        if new_interval > 0:
            interval = new_interval
            return jsonify({"message": f"Interval set to {interval} seconds."})
        else:
            return jsonify({"error": "Interval must be greater than 0."}), 400
    except ValueError:
        return jsonify({"error": "Invalid interval value."}), 400


if __name__ == '__main__':
    app.run(debug=True)
