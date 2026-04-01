import csv
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["inventory_db"]

collection = db["products"]

collection.drop()

with open("products.csv", "r") as file:
    reader = csv.DictReader(file)
    products = []
    for row in reader:
        product = {
            "ProductID": int(row["ProductID"]),
            "Name": row["Name"],
            "UnitPrice": float(row["UnitPrice"]),
            "StockQuantity": int(row["StockQuantity"]),
            "Description": row["Description"]
        }
        products.append(product)

collection.insert_many(products)

print("Done! " + str(len(products)) + " products inserted into MongoDB.")
