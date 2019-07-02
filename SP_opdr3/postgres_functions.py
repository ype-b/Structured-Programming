import psycopg2


#establishes connection with postgres database
def connectToPostgreSQL():
    conn = psycopg2.connect(host="localhost", database="AAIproject", user="postgres", password="pw")
    return conn


def getProdcutById_postgres(data):
    ret_list = []
    conn = connectToPostgreSQL()
    cur = conn.cursor()

    cur.execute("SELECT * FROM product")
    row = cur.fetchone()

    while row is not None:
        if row[0] == data.get("productId"):
            print("FOUND")
            ret_list.append({"_id": row[0], "selling_price" : row[1]})
            cur.close()
            return ret_list

        row = cur.fetchone()

    print("NOT FOUND")
    cur.close()
    conn.close()


#removes id's from list that have the same first 5 characters.
def cleanUpColorDuplicates(list):
    for item_a in list:
        for item_b in list:
            if item_a == item_b:
                continue
            elif item_a[0:4] == item_b[0:4]:
                list.remove(item_b)


def getDataFromTable(table, id):
    ret_list = []

    conn = connectToPostgreSQL()
    cur = conn.cursor()

    cur.execute("SELECT * FROM {}".format(table))
    row = cur.fetchone()

    while row is not None:
        if row[0] == id:
            if len(row) == 2:
                ret_list.append(row[1])
            else:
                ret_list.append(row[1 : len(row)-1])

        row = cur.fetchone()

    cur.close()
    conn.close()
    return ret_list


def getProfile(visitor_id):
    ret_dict = {"visitor_id": visitor_id, "buids" : None, "orders" : [], "viewed_before" : None}

    #store data into the profile with same reusable function
    ret_dict["buids"] = getDataFromTable('visitors_buid', visitor_id)

    for x in range(len(ret_dict["buids"])):
        ret_dict["orders"].append(getDataFromTable('orders', ret_dict["buids"][x]))

    ret_dict["viewed_before"] = getDataFromTable('viewed_before', visitor_id)

    return ret_dict
