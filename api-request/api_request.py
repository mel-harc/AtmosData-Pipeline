import requests

def fetch_data(api_url : str):
    print("Fetching Weather Data From Weatherstack API...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("Response Recieved Successfuly")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An Error Occured: {e}")
        raise