from postgres_functions import connectToPostgreSQL, cleanUpColorDuplicates
from mongodb_functions import getProductsFromList
import random

#searches for products with the same sub_sub_category
def getProductsWithSameCategory(data):
    ret_list = []
    product = None

    conn = connectToPostgreSQL()
    cur = conn.cursor()

    #search for the input product in the table and save its row of data to variable product, so it can then be compared to the other rows in the table.
    cur.execute("SELECT * FROM product")
    row = cur.fetchone()

    while row is not None:
        if row[0] == data.get("productId"):
            product = row
            break
        else:
            row = cur.fetchone()

    #properties is iterated again, now to compare the input product with the other products
    cur.execute("SELECT * FROM product")
    row = cur.fetchone()

    while row is not None:
        if row[4] == product[4] and row[0] != data.get("productId") and (row[5] == product[5] or row[5] == 'unisex'):
            ret_list.append(row[0])

        row = cur.fetchone()

    cur.close()
    conn.close()
    return ret_list


#Searches for products with the same properties
#weight parameter determines how many % properties need to be shared
def getProductsWithSameProperties(data, weight = 0.3):
    ret_list = []
    product = None
    target_points = 0

    conn = connectToPostgreSQL()
    cur = conn.cursor()

    #search for the input product in the table and save its row of data to variable product, so it can then be compared to the other rows in the table.
    cur.execute("SELECT * FROM properties")
    row = cur.fetchone()

    while row is not None:
        if row[0] == data.get("productId"):
            product = row
            break
        else:
            row = cur.fetchone()

    for x in range(2, len(product)):
        if product[x] != 'None':
            target_points += 1

    #properties is iterated again, now to compare the input product with the other products
    cur.execute("SELECT * FROM properties")
    row = cur.fetchone()

    while row is not None:
        points = 0
        for x in range(2, len(row)):
            if row[x] == product[x] and row[x] != 'None':
                points += 1
        if points >= (target_points * weight):
            ret_list.append(row[0])

        row = cur.fetchone()

    cur.close()
    conn.close()
    return ret_list


#main function for the similar products feature
def getSimilarProducts(data):
    #two lists are created for both search criteria (categories and properties)
    list_a = getProductsWithSameCategory(data)
    list_b = getProductsWithSameProperties(data)
    list_ab = list_a + list_b
    ret_list = []

    #many products have duplicate entries for different colors, these are removed
    cleanUpColorDuplicates(list_ab)

    #there are two entries
    temp_set = (set([x for x in list_ab if list_ab.count(x) > 1]))
    for item in temp_set:
        ret_list.append(item)

    random.shuffle(ret_list)
    ret_list = ret_list[0:min(10, len(ret_list))]
    ret_list = getProductsFromList(ret_list)
    return ret_list
