import requests


def get_database_data():
    url = 'https://tul-app-7392a-default-rtdb.europe-west1.firebasedatabase.app/UserData.json'
    resp = requests.get(url)
    return resp.json()