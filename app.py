from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Simulated sensor data (replace with actual sensor readings)
def get_sensor_status():
    # Randomly simulate sensor data (status)
    status = random.choice(['healthy', 'lung_issue', 'diabetes', 'cancer'])
    return status

@app.route('/')
def index():
    # Get the sensor status
    status = get_sensor_status()
    return render_template('main.html', status=status)

@app.route('/status', methods=['GET'])
def status():
    # Send JSON response with sensor status
    status = get_sensor_status()
    return jsonify({"status": status})

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    print("Received data:", data)

    # Simulate normal conditions
    is_normal = all([
        data['mq2']['co'] <= 50,  # Normal CO levels
        data['mq2']['methane'] <= 100,  # Normal Methane levels
        data['mq3']['ethanol'] <= 20,  # Normal Ethanol levels
        data['mq3']['acetone'] <= 10,  # Normal Acetone levels
        data['mq135']['benzene'] <= 5,  # Normal Benzene levels
        data['mq135']['methyl_mercaptan'] <= 2  # Normal Methyl Mercaptan levels
    ])

    detected_diseases = []
    if is_normal:
        detected_diseases.append("Normal: No issues detected")
    else:
        if data['mq2']['co'] > 50:
            detected_diseases.append("High CO levels detected")
        if data['mq2']['methane'] > 100:
            detected_diseases.append("High Methane levels detected")
        if data['mq3']['ethanol'] > 20:
            detected_diseases.append("High Ethanol levels detected")
        if data['mq3']['acetone'] > 10:
            detected_diseases.append("High Acetone levels detected")
        if data['mq135']['benzene'] > 5:
            detected_diseases.append("High Benzene levels detected")
        if data['mq135']['methyl_mercaptan'] > 2:
            detected_diseases.append("High Methyl Mercaptan levels detected")

    advice = "Normal: No action required." if is_normal else "Consult a doctor if symptoms persist."
    gas_ratios = {
        "CO": data['mq2']['co'],
        "Methane": data['mq2']['methane'],
        "Ethanol": data['mq3']['ethanol'],
        "Acetone": data['mq3']['acetone'],
        "Benzene": data['mq135']['benzene'],
        "Methyl Mercaptan": data['mq135']['methyl_mercaptan']
    }

    return jsonify({
        "detected_diseases": detected_diseases,
        "advice": advice,
        "gas_ratios": gas_ratios
    })

if __name__ == "__main__":
    app.run(debug=True)