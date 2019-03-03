import pymongo
import psycopg2

conn = psycopg2.connect( host = "localhost", database = "voordeelshop", user = "postgres", password = "pw" ) #connect to database
cur = conn.cursor() #establish cursor

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['_opop_db']
cur_product = db['products'].find()
cur_visitor = db['visitors'].find()


def clean_db(conn, cur, database):
    query = "DELETE FROM {}".format(database)
    cur.execute(query)
    conn.commit()

def insert_visitor_data (conn, cur, cursor, clear):
    if clear:
        clean_db(conn, cur, "visitor")

    for product in cursor:
        id = product.get('_id')

        query = "INSERT INTO visitor VALUES ( $${}$$) ON CONFLICT DO NOTHING".format(id)

        cur.execute(query)

def insert_product_data (conn, cur, product_list, clear):
    if clear:
        clean_db(conn, cur, "product")
    for product in product_list:
        product_id = product.get("_id")

        selling_price = -1

        if "price" in product:
            product_price = product.get("price")

            if "selling_price" in product_price:
                selling_price = product_price.get("selling_price")

        query = "INSERT  INTO product VALUES ( $${}$$, {} ) ON CONFLICT (_id) DO NOTHING".format(product_id, selling_price)

        cur.execute(query)

insert_visitor_data(conn, cur, cur_visitor, True)
#insert_product_data(conn, cur, cur_product, True)


conn.commit()
cur.close()
conn.close()
