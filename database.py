# https://sparkbyexamples.com/python/python-difference-between-staticmethod-and-classmethod/#:~:text=Difference%20Between%20saticmethod%20vs%20classmethod,-The%20main%20difference&text=A%20staticmethod%20takes%20no%20special,to%20modify%20class%2Dlevel%20attributes.

# https://cosasdedevs.com/posts/metodos-clase-metodos-estaticos-python/#:~:text=Para%20declarar%20un%20m%C3%A9todo%20est%C3%A1tico,staticmethod%20y%20nuestro%20m%C3%A9todo%20est%C3%A1tico.&text=Como%20puedes%20ver%2C%20en%20ning%C3%BAn,acceder%20a%20estos%20sin%20problema.

# https://www.youtube.com/watch?v=9YJr5yLuTZI&t=274s
import os
import json
from typing import Dict

class Database:

    @classmethod
    def select_all(cls):
        # Does the database exist? If not, create it
        if not os.path.isfile('user_table.json'):
            with open('user_table.json', 'w') as f:
                # Inserting an empty array
                json.dump([], f)
        
        # If the file was found
        with open('user_table.json', 'r') as f:
            data = json.load(f)
        return data
    
    @classmethod
    def insert(cls, data: Dict):
        with open('user_table.json', 'w') as f:
            json.dump(data, f)

    @classmethod
    def confirm_last_save(cls):
        with open('user_table.json', 'r') as f:
            data = json.load(f)
        return data[-1]
    
    @classmethod
    def select(cls, user_id: str):
        with open('user_table.json', 'r') as f:
            data = json.load(f)

        for d in data:
            if d["id"] == user_id:
                return d
        
        return []
