import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['_opop_db']

def loadCollection(collection, amount = -1):
    cursor = db[collection].find()
    return_list = []

    if amount == -1:
        for x in cursor:
            return_list.append(x)
    else:
        for x in range(0, amount):
            return_list.append(cursor[x])

    print("{} LOADED".format(collection))

    return return_list


def getPopularProducts():
    return [
        { "_id": "23978", "brand": "8x4", "category": "Gezond & verzorging", "deeplink": "https://www.opisopvoordeelshop.nl/8x4-men-men-beast-deospray-150ml" },
        { "_id": "7225", "brand": "8x4", "category": "Gezond & verzorging", "deeplink": "https://www.opisopvoordeelshop.nl/8x4-heavenly-deospray-150ml" },
        { "_id": "29438", "brand": "1Auto", "category": "Wonen & vrije tijd", "deeplink": "https://www.opisopvoordeelshop.nl/1auto-ruitensproeiervloeistof-zomer-4000ml" },
        { "_id": "9196", "brand": "8x4", "category": "Gezond & verzorging", "deeplink": "https://www.opisopvoordeelshop.nl/8x4-for-men-urban-spirit-150-ml"},
        { "_id": "8570", "brand": "8x4", "category": "Gezond & verzorging", "deeplink": "https://www.opisopvoordeelshop.nl/8x4-unity-150-ml"},
        { "_id": "22309", "brand": "Agfa", "category": "Elektronica & media", "deeplink": "https://www.opisopvoordeelshop.nl/afgaphoto-alkaline-power-batterijen-aa-4-stuks"}
    ]

def getRecentProducts():
    return [
        {"_id": "9196", "brand": "8x4", "category": "Gezond & verzorging", "deeplink": "https://www.opisopvoordeelshop.nl/8x4-for-men-urban-spirit-150-ml"},
        {"_id": "8570", "brand": "8x4", "category": "Gezond & verzorging", "deeplink": "https://www.opisopvoordeelshop.nl/8x4-unity-150-ml"}
    ]

def getPersonalProducts(session):
    print("Recommendations for session: {}".format(session['sessionId']))
    return [
        {"_id": "9196", "brand": "8x4", "category": "Gezond & verzorging", "deeplink": "https://www.opisopvoordeelshop.nl/8x4-for-men-urban-spirit-150-ml"},
        {"_id": "8570", "brand": "8x4", "category": "Gezond & verzorging", "deeplink": "https://www.opisopvoordeelshop.nl/8x4-unity-150-ml"},
        {"_id": "22309", "brand": "Agfa", "category": "Elektronica & media", "deeplink": "https://www.opisopvoordeelshop.nl/afgaphoto-alkaline-power-batterijen-aa-4-stuks"}
    ]

def getProduct(input_id):
    print("Recommendations for session: {}".format(input_id['sessionId']))
    products = loadCollection('products', 10)

    for x in len(products):
        if products[x].get("_id") == input_id.get("sessionID"):
            return [products[x]]

    return []

def findItem(collection, parameter, query):
    for x in range(0, len(collection)):
        if str(collection[x].get(parameter)) == str(query):
            return collection[x]
    print("NOT FOUND")

    return []

def getRecommendedProducts(data):
    visitor = findItem(loadCollection('visitors', 20), '_id', data.get("loginId"))
    recommendation_list = visitor.get('recommendations').get('similars')
    products = loadCollection('products')
    return_list = []

    for product in products:
        if product.get("_id") in recommendation_list:
            return_list.append(product)

    return return_list

def getProductsOOS():
    products = loadCollection('products')
    return_list = []

    for x in range(0, len(products)):
        try:
            if products[x].get("properties").get("availability") == "0":
                return_list.append(products[x])
        except AttributeError:
            pass

    return return_list

def getSimilarProducts(data):
    products = loadCollection('products')
    product = findItem(products, '_id', data.get("productId"))
    property_x = product.get("properties")
    return_list = []
    exceptions = ["availability", "klacht", "tax", "inhoud", "mid", "online_only", "shopcart_promo_item", "shopcart_promo_price", "stock"]

    for x in range(0, len(products)):
        if product.get("_id") == products[x].get("_id"):
            continue

        points = 0
        property_y = products[x].get("properties")

        for property in property_x:
            if property in exceptions:
                continue
            try:
                if property_x.get(property) == property_y.get(property):
                    if property_x.get(property) is not None:
                        points += 1
            except AttributeError:
                pass

        if points >= 7:
            return_list.append(products[x])

    return return_list
