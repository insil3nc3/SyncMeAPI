from fastapi import FastAPI, HTTPException
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()

# Подключение к MongoDB Atlas
uri = URI
client = MongoClient(uri, server_api=ServerApi('1'))

# Подключение к базе данных и коллекции
db = client["zamkid_db"]
collection = db["users"]

# Роуты FastAPI

@app.post("/register/")
def register(user: str, password: str):
    if collection.find_one({"user": user}):
        raise HTTPException(status_code=400, detail="User already exists")
    collection.insert_one({"user": user, "password": password, "link": "empty"})
    return {"message": "User registered successfully"}

@app.post("/login/")
def login(user: str, password: str):
    current_user = collection.find_one({"user": user})
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user["password"] != password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"message": "Login successful"}

@app.get("/get_link/")
def get_link(user: str):
    current_user = collection.find_one({"user": user})
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"link": current_user["link"]}

@app.put("/set_link/")
def set_link(user: str, link: str):
    result = collection.update_one({"user": user}, {"$set": {"link": link}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Link updated successfully"}

@app.post("/logout/")
def logout(user: str):
    result = collection.update_one({"user": user}, {"$set": {"user": "Unknown"}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User logged out successfully"}
