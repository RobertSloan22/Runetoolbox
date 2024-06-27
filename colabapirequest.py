import requests
import pandas as pd

# URL of the Flask server
url = "http://localhost:3000/runes"

# Fetch the data from the server
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
else:
    raise Exception(f"Failed to fetch data: {response.text}")

