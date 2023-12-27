from fastapi import FastAPI, HTTPException
from typing import Text, Optional
from uuid import uuid4 as uuid # https://docs.python.org/3/library/uuid.html
from pydantic import BaseModel
from datetime import datetime
from database import Database
from copy import copy

app = FastAPI()

class User(BaseModel):
    id: Optional[str] = None
    name: str
    age: str
    profession: str
    about: Optional[Text] = None
    married: bool = False
    registered_at: str = str(datetime.now())

@app.get("/")
def read_root():
    return {"message": "Welcome to my REST API"}

@app.get("/users")
def get_users():
    return Database.select_all()

@app.get("/users/{user_id}")
def get_user(user_id: str):
    user = Database.select(user_id)

    if len(user) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users")
def create_user(user: User):
    user.id = str(uuid()) # To create an unique random ID

    users = Database.select_all()
    users.append(dict(user)) # model_dump_json() or model_dump() == dict() https://docs.pydantic.dev/latest/migration/ or https://docs.pydantic.dev/dev-v2/usage/serialization/#modelmodel_dump_json
    Database.insert(users)

    confirmed_user = Database.confirm_last_save()
    
    return {"message": "User created successfully", "user": confirmed_user}

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    users = Database.select_all()

    for index, user in enumerate(users):
        if user["id"] == user_id:
            deleted_user = copy(user)
            users.pop(index)
            Database.insert(users)
            return {"message": "User deleted successfully", "user": deleted_user}

    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
def update_user(user_id: str, updated_user: User):
    users = Database.select_all()

    for index, user in enumerate(users):
        if user["id"] == user_id:
            users[index]["name"] = updated_user.name
            users[index]["age"] = updated_user.age
            users[index]["profession"] = updated_user.profession
            users[index]["about"] = updated_user.about
            users[index]["married"] = updated_user.married
            Database.insert(users)
            return {"message": "User updated successfully", "user": users[index]}

    raise HTTPException(status_code=404, detail="User not found")