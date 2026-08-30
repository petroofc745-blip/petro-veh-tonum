from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    key = request.args.get('key')
    vehicle = request.args.get('vehicle')

    if not key or not vehicle:
        return jsonify({"error": "Missing key or vehicle parameter"}), 400

    if key != "FREE2DAY":
        return jsonify({"error": "Invalid API Key"}), 401

    try:
        target_url = f"https://vehicletonum.suryajasoos-4fe.workers.dev/?type=vehicle_num&term={vehicle}"
        resp = requests.get(target_url)
        mobile_number = resp.text.strip()

        # JSON response format
        data = {
            "status": "success",
            "query": vehicle,
            "mobile_number": mobile_number,
            "developer": "@coderpetro",
            "expiry_on": "09-01-2026"
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Failed to fetch data or not found"}), 500
