from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["inventory_db"]
collection = db["products"]

@app.get("/test")
def test():
    try:
        product = collection.find_one({"ProductID": 1001}, {"_id": 0})
        return {"result": str(product)}
    except Exception as e:
        return {"error": str(e)}
