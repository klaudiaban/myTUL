import requests

url = 'https://tul-app-7392a-default-rtdb.europe-west1.firebasedatabase.app/UserData.json'
resp = requests.get(url)
print(resp.json())