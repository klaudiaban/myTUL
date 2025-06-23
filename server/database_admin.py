import firebase_admin
from firebase_admin import db, credentials
from datetime import datetime
import random
import calculate
import sqlite3

#THIS IS CODE FOR THE ADMIN APP WITH THE CAMERAS
#THIS WILL NOT BE INCLUDED IN THE APP
#THIS ALSO NEEDS A JSON KEY FILE THAT IS LOCAL AND CANNOT BE ON GITHUB

cred = credentials.Certificate("tul-app-7392a-firebase-adminsdk-fbsvc-999f09589f.json") #key file
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL':"https://tul-app-7392a-default-rtdb.europe-west1.firebasedatabase.app/"}) # connection to the realtime database

ref = db.reference('/')
print(ref.get())
current = db.reference('/UserData/Current')
stats = db.reference('/UserData/Stats')
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
safe_key = str(timestamp)

conn = sqlite3.connect('alltime.db') #connection to the local sqlite database for alltime data
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place TEXT NOT NULL,
    amount INTEGER,
    date DATETIME NOT NULL
)
''')
conn.commit()

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


def insert_into_database(room, amount, date):
    cursor.execute("INSERT INTO data (place, amount, date) VALUES (?, ?, ?)", (room, amount, date))
    conn.commit()

def set_realtime_data(current_data):
    current.set(current_data)

def update_stats(stats_data):
    stats.set(stats_data)


def calculate_stats():
    calculate.calculate_stats()