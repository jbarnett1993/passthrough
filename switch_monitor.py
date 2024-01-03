import requests

# Your credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
scope = 'YOUR_SCOPE'  # Optional, space-delimited if multiple scopes

# OAuth 2.0 endpoint
url = 'https://idfs.gs.com/as/token.oauth2'

# Payload with the required parameters
payload = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope
}

# Make the POST request
response = requests.post(url, data=payload)

# Check if the request was successful
if response.status_code == 200:
    # Extract the token from the response
    token = response.json().get('access_token')
    print("Authentication token:", token)
else:
    print("Failed to retrieve token:", response.status_code, response.text)