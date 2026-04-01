from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import requests
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

# connect to mongodb
client = MongoClient("mongodb://localhost:27017/")
db = client["inventory_db"]
collection = db["products"]


# product model
class Product(BaseModel):
    ProductID: int
    Name: str
    UnitPrice: float
    StockQuantity: int
    Description: str


@app.get("/")
def home():
    return {"message": "Inventory API is running"}


# get one product
@app.get("/getSingleProduct")
def get_single_product(ProductID: int):
    product = collection.find_one({"ProductID": ProductID}, {"_id": 0})
    if product is None:
        return {"error": "Product not found"}
    return product


# get all products
@app.get("/getAll")
def get_all():
    products = list(collection.find({}, {"_id": 0}))
    return products


# add a new product
@app.post("/addNew")
def add_new(product: Product):
    collection.insert_one(product.dict())
    return {"message": "Product added successfully"}


# delete one product
@app.delete("/deleteOne")
def delete_one(ProductID: int):
    result = collection.delete_one({"ProductID": ProductID})
    if result.deleted_count == 0:
        return {"error": "Product not found"}
    return {"message": "Product deleted successfully"}


# search by first letter
@app.get("/startsWith")
def starts_with(letter: str):
    products = list(collection.find(
        {"Name": {"$regex": "^" + letter, "$options": "i"}},
        {"_id": 0}
    ))
    return products


# paginate by id range
@app.get("/paginate")
def paginate(startID: int, endID: int):
    products = list(collection.find(
        {"ProductID": {"$gte": startID, "$lte": endID}},
        {"_id": 0}
    ).limit(10))
    return products


# convert usd to euro
@app.get("/convert")
def convert(ProductID: int):
    product = collection.find_one({"ProductID": ProductID}, {"_id": 0})

    if product is None:
        return {"error": "Product not found"}

    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    data = response.json()
    euro_rate = data["rates"]["EUR"]

    euro_price = round(product["UnitPrice"] * euro_rate, 2)

    return {
        "ProductID": product["ProductID"],
        "Name": product["Name"],
        "PriceUSD": product["UnitPrice"],
        "PriceEUR": euro_price
    }