import os
import json

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


def ensure_directory(path):
    os.makedirs(path, exist_ok=True)
