import firebase_admin
from firebase_admin import db, credentials
from datetime import datetime
import random

#THIS IS CODE FOR THE ADMIN APP WITH THE CAMERAS
#THIS WILL NOT BE INCLUDED IN THE APP
#THIS ALSO NEEDS A JSON KEY FILE THAT IS LOCAL AND CANNOT BE ON GITHUB

cred = credentials.Certificate("tul-app-7392a-firebase-adminsdk-fbsvc-999f09589f.json") #key file
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL':"https://tul-app-7392a-default-rtdb.europe-west1.firebasedatabase.app/"})

ref = db.reference('/')
print(ref.get())
current = db.reference('/UserData/Current')
stats = db.reference('/UserData/Stats')
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
safe_key = str(timestamp)
data = {"place": "Biblioteka", "amount": random.randint(0, 15)}
rooms ={
    "Biblioteka": db.reference('/AdminData/AllTime/Biblioteka'),
    "Lodex": db.reference('/AdminData/AllTime/Lodex'),
}

# realtime data update
current_data = {
    "Biblioteka":
        {
            "date": datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
            "amount": random.randint(0, 15),
        },
    "Lodex":
        {
            "date": datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
            "amount": random.randint(0, 15),
        },
}

#once a day average calculated data
stats_data = {
    "Biblioteka":
        {
        "Monday":
            {
                "7":
                    {
                        "amount": 1,
                    },
                "8":
                    {
                        "amount": 3,
                    },
                "9":
                    {
                        "amount": 3,
                    },
                "10":
                    {
                        "amount": 3,
                    },
                "11":
                    {
                        "amount": 3,
                    },
                "12":
                    {
                        "amount": 3,
                    },
                "13":
                    {
                        "amount": 3,
                    },
                "14":
                    {
                        "amount": 3,
                    },
                "15":
                    {
                        "amount": 3,
                    },
                "16":
                    {
                        "amount": 3,
                    },
                "17":
                    {
                        "amount": 3,
                    },
                "18":
                    {
                        "amount": 3,
                    },
                "19":
                    {
                        "amount": 3,
                    },
                "20":
                    {
                        "amount": 3,
                    },
            },
        "Tuesday":
            {
                "7":
                    {
                        "amount": 1,
                    },
                "8":
                    {
                        "amount": 3,
                    },
                "9":
                    {
                        "amount": 3,
                    },
                "10":
                    {
                        "amount": 3,
                    },
                "11":
                    {
                        "amount": 3,
                    },
                "12":
                    {
                        "amount": 3,
                    },
                "13":
                    {
                        "amount": 3,
                    },
                "14":
                    {
                        "amount": 3,
                    },
                "15":
                    {
                        "amount": 3,
                    },
                "16":
                    {
                        "amount": 3,
                    },
                "17":
                    {
                        "amount": 3,
                    },
                "18":
                    {
                        "amount": 3,
                    },
                "19":
                    {
                        "amount": 3,
                    },
                "20":
                    {
                        "amount": 3,
                    },
            }
        }
    }


def insert_data(table, header, data):
    table.child(header).set(data)

def set_realtime_data():
    current.set(current_data)

def update_stats():
    stats.set(stats_data)

