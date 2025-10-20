import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    notes = data.get("notes", "").strip()

    if not notes:
        return jsonify({"error": "No notes provided"}), 400

    try:
        # Send to Hugging Face API
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": notes})
        result = response.json()

        # Check for HF errors
        if isinstance(result, dict) and "error" in result:
            return jsonify({"error": f"Hugging Face API error: {result['error']}"}), 500

        # Check if we got a summary
        if isinstance(result, list) and len(result) > 0 and "summary_text" in result[0]:
            summary = result[0]["summary_text"]
            return jsonify({"summary": summary})
        else:
            return jsonify({"error": f"Unexpected response format: {result}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

