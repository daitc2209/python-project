from pymongo import MongoClient

myclient = MongoClient("mongodb://db:27017/")

mydb = myclient["education_dev"]
myUser = mydb["users"]
myProduct = mydb["products"]
myCart = mydb["carts"]
myOrder = mydb["orders"]
myOrderDetail = mydb["order_details"]
myFavor = mydb['favorites']