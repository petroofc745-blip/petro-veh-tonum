from flask import Flask, request, jsonify
import requests
import json

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
        raw_text = resp.text.strip()

        # Parse raw response if it's a JSON string, else fallback
        mobile_number = "Not Found"
        try:
            parsed_data = json.loads(raw_text)
            if isinstance(parsed_data, dict):
                mobile_number = parsed_data.get("mobile_no", "Not Found")
        except:
            mobile_number = raw_text

        # Required clean output format
        data = {
            "query": vehicle,
            "mobile number": mobile_number,
            "developer": "@coderpetro",
            "expiry on": "09-01-2026"
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Failed to fetch data"}), 500
