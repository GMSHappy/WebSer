from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Union
import requests

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://192.168.1.20:27017/")
db = client["inventory_db"]
collection = db["products"]

#Pydantic model for adding a new product
class Product(BaseModel):
    ProductID: int
    Name: str
    UnitPrice: float
    StockQuantity: int
    Description: str


#Get a single product by ID
@app.get("/getSingleProduct")
def get_single_product(ProductID: int):
    product = collection.find_one({"ProductID": ProductID}, {"_id": 0})
    if product is None:
        return {"error": "Product not found"}
    return product


#Get all products
@app.get("/getAll")
def get_all():
    products = list(collection.find({}, {"_id": 0}))
    return products


#Add a new product
@app.post("/addNew")
def add_new(product: Product):
    collection.insert_one(product.dict())
    return {"message": "Product added successfully"}


#Delete a product by ID
@app.delete("/deleteOne")
def delete_one(ProductID: int):
    result = collection.delete_one({"ProductID": ProductID})
    if result.deleted_count == 0:
        return {"error": "Product not found"}
    return {"message": "Product deleted successfully"}


#Get all products starting with a letter
@app.get("/startsWith")
def starts_with(letter: str):
    products = list(collection.find(
        {"Name": {"$regex": "^" + letter, "$options": "i"}},
        {"_id": 0}
    ))
    return products


#Paginate products by ID range
@app.get("/paginate")
def paginate(startID: int, endID: int):
    products = list(collection.find(
        {"ProductID": {"$gte": startID, "$lte": endID}},
        {"_id": 0}
    ).limit(10))
    return products


#Convert product price from USD to EUR
@app.get("/convert")
def convert(ProductID: int):
    product = collection.find_one({"ProductID": ProductID}, {"_id": 0})
    if product is None:
        return {"error": "Product not found"}
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    rate = response.json()["rates"]["EUR"]
    price_in_euros = round(product["UnitPrice"] * rate, 2)
    return {"ProductID": ProductID, "Name": product["Name"], "PriceUSD": product["UnitPrice"], "PriceEUR": price_in_euros}