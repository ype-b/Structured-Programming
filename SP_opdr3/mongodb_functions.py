import pymongo

def connectToMongoDB():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client['_opop_db']
    return db

def loadCollectionIntoList(collection, amount = -1):
    db = connectToMongoDB()
    cursor = db[collection].find()
    return_list = []

    if amount == -1:
        for x in cursor:
            return_list.append(x)
    else:
        for x in range(0, amount):
            return_list.append(cursor[x])

    return return_list

def findItem(collection, parameter, query):
    for x in range(0, len(collection)):
        if str(collection[x].get(parameter)) == str(query):
            return collection[x]

    return []

def getProductByID(data):
    ret_list = []

    ret_list.append(findItem(loadCollectionIntoList("products"), "_id", data.get("productId")))
    return ret_list


#takes a list of id's, fetches them from mongodb and returns a list of of those products in dictionaries that can be displayed on the front-end.
def getProductsFromList(list):
    ret_list = []

    x = 0
    while x < len(list):
        for product in product_list:
            if product.get("_id") in list:
                ret_list.append(product)
                x += 1

    return ret_list

product_list = loadCollectionIntoList('products')
