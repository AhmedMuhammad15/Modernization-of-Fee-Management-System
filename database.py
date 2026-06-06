import json
import os

FILE_NAME = "students_db.json"

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as f:
            try: return json.load(f)
            except: return []
    return []

def save_data(data):
    with open(FILE_NAME, 'w') as f:
        json.dump(data, f, indent=4)