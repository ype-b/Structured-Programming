from postgres_functions import connectToPostgreSQL, cleanUpColorDuplicates, getProfile
from mongodb_functions import getProductsFromList
import random

def getProductsBasedOnBrand(data):
    visitor_id = data.get("visitorId")
    visitor_profile = getProfile(visitor_id)
    visitor_ordered = []
    ret_list = []
    product_list = []
    counter_list = []
    product = None

    #prepare a list of items the visitor has ordered before so it can be more easily checked later
    for x in range(len(visitor_profile["orders"])):
        for y in range(len(visitor_profile["orders"][x])):
            visitor_ordered.append(visitor_profile["orders"][x][y])

    for x in range(len(visitor_ordered)):
        if visitor_ordered[x] not in product_list:
            product_list.append(visitor_ordered[x])
            counter_list.append(1)
        else:
            counter_list[product_list.index(visitor_ordered[x])] += 1

    most_purchased_product = product_list[counter_list.index(max(counter_list))]

    # search for the input product in the table and save its row of data to variable product, so it can then be compared to the other rows in the table.
    conn = connectToPostgreSQL()
    cur = conn.cursor()

    cur.execute("SELECT * FROM product")
    row = cur.fetchone()

    while row is not None:
        if row[0] == most_purchased_product:
            product = row
            break
        else:
            row = cur.fetchone()

    cur.execute("SELECT * FROM product")
    row = cur.fetchone()

    while row is not None:
        if row[1] == product[1] and row[0] != data.get("productId") and (row[5] == product[5] or row[5] == 'unisex'):
            ret_list.append(row[0])

        row = cur.fetchone()

    cur.close()
    conn.close()

    cleanUpColorDuplicates(ret_list)
    random.shuffle(ret_list)
    ret_list = ret_list[0:min(5, len(ret_list))]
    ret_list = getProductsFromList(ret_list)
    return ret_list
