import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, render_template , request , jsonify 
import time
from datetime import datetime
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Creating flask app
app = Flask(__name__)

# Path to the JSON file containing the regions data
DATA_FILE = 'zones.json'
last_sent_time = 0
# Path to your service account key file
service_account_path = "csite-assistant-firebase-adminsdk-p20ha-43cee8491c.json"

# Initialize the Firebase Admin SDK

cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred , {
    'databaseURL':"https://csite-assistant-default-rtdb.firebaseio.com/"
})

def log_data(person_count):
    global last_sent_time
    current_time = time.time()
    if last_sent_time is None or current_time - last_sent_time >= 5:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("log.txt", "a") as file:
            file.write(f"{timestamp} - {person_count}\n")
        last_sent_time = current_time
    else:
        print("Not enough time has passed since the last upload")

def load_zones():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_zones(zones):
    with open(DATA_FILE, 'w') as f:
        json.dump(zones, f)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/work_assign.html')
def work_assign():
    return render_template('zones.html')


@app.route('/add_zone', methods=['POST'])
def add_zone():
    data = request.get_json()
    save_zones(data)
    return jsonify({'success': True})

@app.route('/get_zones', methods=['GET'])
def get_zones():
    zones = load_zones()
    return jsonify(zones)

@app.route('/api/zones')
def get_zones2():
    try:
        with open('zones.json', 'r') as f:
            zones = json.load(f)
        return jsonify(zones), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/reset_zones', methods=['POST'])
def reset_zones():
    try:
        # Clear zones.json by writing empty array
        with open('zones.json', 'w') as f:
            json.dump([], f)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/compliance_data')
def compliance_data():
    data = db.reference('/').get()
    transformed_data = []
    if 'object_detections' in data:
        for detection in data['object_detections']:
            transformed_data.append({
                "label": detection.get("label", "Unknown"),
                "confidence": round(detection.get("confidence", 0), 2),
                "boundingBox": {
                    "x1": int(detection.get("boundingBox", {}).get("x1", 0) * 1000),
                    "y1": int(detection.get("boundingBox", {}).get("y1", 0) * 1000),
                    "x2": int(detection.get("boundingBox", {}).get("x2", 0) * 1000),
                    "y2": int(detection.get("boundingBox", {}).get("y2", 0) * 1000),
                }
            })
    print(transformed_data)
    return jsonify({"detections": transformed_data})

@app.route('/api/object_detections')
def get_object_detections():
    object_detections = db.reference('/').get()
    print("Object Detections Data:", object_detections)  # Debug Statement

    if not object_detections or 'object_detections' not in object_detections:
        return jsonify({'labels': [], 'counts': []}), 200

    detections = object_detections['object_detections']
    label_counts = {}

    personflag = 0
    
    for detection in detections:
        if isinstance(detection, dict):
            label = detection.get('label', 'Unknown')
            if label == 'Person':
                personflag = 1
            label_counts[label] = label_counts.get(label, 0) + 1
        else:
            print(f"Invalid detection format: {detection}")

    labels = list(label_counts.keys())
    counts = list(label_counts.values())
    
    # log here
    if personflag == 1:
        person_count = label_counts['Person']
    else:
        person_count = 0
    
    log_data(person_count)
    
    return jsonify({'labels': labels, 'counts': counts}), 200

@app.route('/api/person_centers')
def get_person_centers():
    object_detections = db.reference('/').get()
    print("Object Detections Data:", object_detections)  # Debug Statement

    if not object_detections or 'object_detections' not in object_detections:
        return jsonify({'points': []}), 200

    detections = object_detections['object_detections']
    person_centers = []

    # Define labels that represent a person
    person_labels = ['Person']

    # Get centers of all person-related detections
    for detection in detections:
        if isinstance(detection, dict) and detection.get('label') in person_labels:
            bbox = detection.get('boundingBox', {})
            center_x = (bbox.get('x1', 0) + bbox.get('x2', 0)) / 2
            center_y = (bbox.get('y1', 0) + bbox.get('y2', 0)) / 2
            person_centers.append({'x': center_x, 'y': center_y})

    # Sort by x coordinate to connect points left to right
    person_centers.sort(key=lambda p: p['x'])
    
    return jsonify({'points': person_centers}), 200

@app.route('/log.html')
def display_log():
    return render_template('log.html')

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
        print("zsadfg")
        return jsonify({"error": "log.txt not found"}), 404

    # if not timestamps or not person_counts:
    #     return jsonify({"error": "No data available for graph"}), 400
    print("qwertyuiop")
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

admin_email = "alokamvarun@gmail.com"
admin_name = "Varun Alokam"

@app.route('/send_email' , methods=['POST'])
def send_alert_email():
    """
    Sends an email alert to the admin if non-compliance exceeds 50% of personnel count.
    """
    data = request.json
    non_compliant_count = data.get('param1', 'default1')
    total_personnel = data.get('param2', 'default2')

    if total_personnel == 0:  # Handle edge case where total_personnel might be 0
        return jsonify({
            "status": "error",
            "message": "Total personnel count cannot be zero."
        }), 400
    
    non_compliance_percentage = (non_compliant_count / total_personnel) * 100
    
    if non_compliance_percentage > 50:
        subject = "Safety Non-Compliance Alert"
        body = (f"Dear {admin_name},\n\n"
                f"Alert: More than 50% of the personnel on site are not compliant.\n"
                f"Total Personnel Detected: {total_personnel}\n"
                f"Non-Compliant Personnel: {non_compliant_count}\n"
                f"Non-Compliance Percentage: {non_compliance_percentage:.2f}%\n\n"
                f"Please take immediate action to ensure safety compliance.\n\n"
                f"Regards,\nSafety Monitoring System")
        
        msg = MIMEMultipart()
        msg['From'] = "constructionanalytics569@gmail.com" 
        msg['To'] = admin_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587) 
            server.starttls()
            server.login("constructionanalytics569@gmail.com", "jcnp vtrv dbhn jsxc")
            server.sendmail("constructionanalytics569@gmail.com",admin_email,msg.as_string())
            server.quit()
            print("Alert email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")
        return jsonify({
            "status":"success"
        }) , 200
    else:
        return jsonify({
            "status": "error",
            "message": "Non-compliance percentage is below the threshold."
        }), 200

# detected_personnel = 100  
# non_compliant = 60  

# send_alert_email(non_compliant, detected_personnel)


if __name__ == '__main__':
    app.run(debug=True)