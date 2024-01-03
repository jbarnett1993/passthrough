import requests

# Your credentials
client_id = '5856b7c9c08140d69313b1b723108c25'
client_secret = 'ff46deb0a3ca4ce3ecd4af97b083072e10be41eb48441921984130a0ad93a7c8'
scope = 'read_financial_data read_product_data read_user_profile'  # Optional, space-delimited if multiple scopes

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