import requests

# Configuration
SUPSET_URL = "https://superset-on-render-fchx.onrender.com"  # Replace with your Superset URL
USERNAME = "admin"
PASSWORD = "admin"
LOGIN_URL = f"{SUPSET_URL}/api/v1/security/login"  # Fixed endpoint
CSRF_TOKEN_URL = f"{SUPSET_URL}/api/v1/security/csrf_token/"
API_REQUEST_URL = f"{SUPSET_URL}/api/v1/some_endpoint/"  # Your target API

def login():
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "provider": "db",
    }
    session = requests.Session()
    response = session.post(LOGIN_URL, json=payload)  # Send as JSON

    if response.status_code == 200:
        print("Login successful! Cookies:", session.cookies.get_dict())
        return session
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def get_csrf_token(session):
    response = session.get(CSRF_TOKEN_URL)
    if response.status_code == 200:
        csrf_token = response.json().get("result")
        if csrf_token:
            print("CSRF token retrieved:", csrf_token)
            return csrf_token
    print(f"CSRF token fetch failed: {response.status_code} - {response.text}")
    return None

def make_post_request(session, csrf_token):
    headers = {
        "X-CSRFToken": csrf_token,
        "Content-Type": "application/json",
    }
    payload = {"key": "value"}  # Customize your payload

    response = session.post(API_REQUEST_URL, headers=headers, json=payload)
    if response.status_code == 200:
        print("POST request succeeded!")
    else:
        print(f"POST failed: {response.status_code} - {response.text}")

def main():
    session = login()
    if not session:
        return  # Exit if login fails

    csrf_token = get_csrf_token(session)
    if not csrf_token:
        return  # Exit if CSRF fails

    make_post_request(session, csrf_token)

if __name__ == "__main__":
    main()
