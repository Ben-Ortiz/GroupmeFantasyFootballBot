import requests

def fetch_data():
    url = 'http://espn-fantasy-football-api.s3-website.us-east-2.amazonaws.com/'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)  # Print raw response content
        # Attempt to parse JSON if the content seems to be in JSON format
        try:
            data = response.json()
            return data
        except ValueError:
            print("Response is not in JSON format")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

data = fetch_data()
