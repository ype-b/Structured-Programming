import psycopg2
from postgres_functions import connectToPostgreSQL
from mongodb_functions import getProductsFromList

def getMostPurchasedProducts():
    ret_list = []

    conn = connectToPostgreSQL()
    cur = conn.cursor()

    cur.execute("SELECT * FROM populair")
    row = cur.fetchone()
    while len(ret_list) < 10:
        ret_list.append(row[0])
        row = cur.fetchone()

    cur.close()
    conn.close()

    ret_list = getProductsFromList(ret_list)
    return ret_list


def insertPostgres(cur,values,tabel,conn):
    try:
        sql = 'INSERT INTO ' + tabel + ' VALUES (' + values + ')'
        cur.execute(sql)
        conn.commit()
    except psycopg2.IntegrityError:
        print(sql)
        conn.commit()


def loadMostPurchasedProductsIntoDatabase():
    conn = connectToPostgreSQL()
    cur = conn.cursor()

    product_list = []
    counter_list = []

    sorted_product_list = []
    sorted_product_list_counter = []

    cur.execute("SELECT * FROM orders")
    row = cur.fetchone()

    while row is not None:
        if row[1] not in product_list:
            product_list.append(row[1])
            counter_list.append(1)
        else:
            counter_list[product_list.index(row[1])] += 1

        row = cur.fetchone()

    x = len(product_list)

    while x:
        most_sold_id = product_list[counter_list.index(max(counter_list))]
        most_sold_count = max(counter_list)

        sorted_product_list.append(most_sold_id)
        sorted_product_list_counter.append(most_sold_count)

        counter_list.remove(most_sold_count)
        product_list.remove(most_sold_id)

        x -= 1

    for index in range(len(sorted_product_list)):
        values= '\''+sorted_product_list[index]+'\''+','+str(sorted_product_list_counter[index])
        insertPostgres(cur,values,'populair',conn)

    cur.close()
    conn.close()
