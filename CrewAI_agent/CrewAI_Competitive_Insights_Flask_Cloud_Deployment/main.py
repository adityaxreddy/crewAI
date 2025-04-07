import time
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

CORS(
    app=app,
    resources={
        r"/*": {
            "origins": [
                "*", 
            ]
        }
    },
)

def fetch_from_crewai(product, company):
    """
    1. GET request for authentication
    2. POST to kickoff the analysis using provided product and company
    3. Poll the status endpoint until state == 'SUCCESS'
    4. Return the final success response JSON
    """
    bearer_token = os.getenv("BEARER_TOKEN")
    base_url = os.getenv("BASE_URL")
    
    # 1) GET request to /inputs (for authentication or initial check)
    auth_url = f"{base_url}/inputs"
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    auth_response = requests.get(auth_url, headers=headers)
    auth_response.raise_for_status()
    
    # 2) POST request to /kickoff with the input data
    kickoff_url = f"{base_url}/kickoff"
    post_data = {
        "inputs": {
            "product": product,
            "company": company
        }
    }
    kickoff_response = requests.post(
        kickoff_url,
        headers={
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        },
        json=post_data
    )
    kickoff_response.raise_for_status()
    
    kickoff_id = kickoff_response.json().get("kickoff_id")
    
    if not kickoff_id:
        raise ValueError("No kickoff_id returned from the /kickoff endpoint.")
    
    # 3) Poll the /status/<kickoff_id> endpoint until 'state' == 'SUCCESS'
    status_url = f"{base_url}/status/{kickoff_id}"
    
    while True:
        status_response = requests.get(status_url, headers=headers)
        status_response.raise_for_status()
        status_json = status_response.json()
        
        current_state = status_json.get("state", "")
        
        if current_state == "SUCCESS":
            result_json = {
                "status": "SUCCESS",
                "data": status_json['result']
            }
            return json.dumps(result_json)
        
        time.sleep(2)

@app.route(rule="/public/test-connection", methods=["GET"])
@cross_origin(origins="*")
def test_connection() -> str:
    """
    .
    """
    return "CONNECTED"

@app.route("/crewai", methods=["POST"])
def main():
    data = request.get_json()
    product = data.get("product")
    company = data.get("company")

    final_response = fetch_from_crewai(product, company)

    return final_response


if __name__ == "__main__":
    app.run(debug=True)