import os
import requests
import json
import sys

# Get credentials from environment variables or command line
BASE_URL = os.getenv("BASE_URL", sys.argv[1] if len(sys.argv) > 1 else "https://superset-on-render-fchx.onrender.com")
USERNAME = os.getenv("USERNAME", sys.argv[2] if len(sys.argv) > 2 else "admin")
PASSWORD = os.getenv("PASSWORD", sys.argv[3] if len(sys.argv) > 3 else "admin")
CHART_ID = int(os.getenv("CHART_ID", sys.argv[4] if len(sys.argv) > 4 else "91"))

session = requests.Session()
 
# 1. Login
login_payload = {
    "username": USERNAME,
    "password": PASSWORD,
    "provider": "db",
    "refresh": True,
}
resp = session.post(f"{BASE_URL}/api/v1/security/login", json=login_payload)
access_token = resp.json().get("access_token")
 
# 2. Test token via /me
me_url = f"{BASE_URL}/api/v1/me"
me_resp = session.get(me_url, headers={"Authorization": f"Bearer {access_token}"})
 
# 3. Get CSRF token
csrf_resp = session.get(
    f"{BASE_URL}/api/v1/security/csrf_token/",
    headers={"Authorization": f"Bearer {access_token}"}
)
csrf_token = csrf_resp.json().get("result")
session.cookies.set("csrf_token", csrf_token)
 
# 4. Get chart metadata to ensure access
chart_url = f"{BASE_URL}/api/v1/chart/{CHART_ID}"
chart_resp = session.get(chart_url, headers={"Authorization": f"Bearer {access_token}"})
 
# 5. Get chart data
headers = {
    "Authorization": f"Bearer {access_token}",
    "X-CSRFToken": csrf_token,
    "Content-Type": "application/json",
    "Referer": BASE_URL,
}
form_data = {"slice_id": CHART_ID}
explore_url = f"{BASE_URL}/superset/explore_json/"
 
data_resp = session.post(explore_url, headers=headers, json=form_data)
# Ensure chart_resp contains a valid JSON response
if chart_resp.status_code == 200 and chart_resp.json() is not None:
    result = chart_resp.json().get("result", {})
    query_context_str = result.get("query_context")
   
    if query_context_str:
        query_context = json.loads(query_context_str)
        data_url = f"{BASE_URL}/api/v1/chart/data"
 
        data_resp = session.post(
            data_url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-CSRFToken": csrf_token,
                "Content-Type": "application/json",
                "Referer": BASE_URL,
            },
            json=query_context,
        )
 
        print("Chart data status:", data_resp.status_code)
        print("Chart data:", data_resp.json())
    else:
        print("Error: 'query_context' is missing or invalid in the chart response.")
else:
    print("Error: Invalid chart response or missing query context.")

# At the end, print the results as JSON
print(json.dumps({
    "status": data_resp.status_code,
    "data": data_resp.json()
}))
