import pymongo
import psycopg2
from products import loadCollectionIntoList

post_conn = psycopg2.connect( host = "localhost", database = "voordeelshop", user = "postgres", password = "pw" ) #connect to database
post_cur = post_conn.cursor() #establish cursor

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client['_opop_db']


def clean_db(post_conn, post_cur, database):
    query = "DELETE FROM {}".format(database)
    post_cur.execute(query)
    post_conn.commit()

def insert_visitor_data (post_conn, post_cur, visitor_list, clear = False):
    if clear:
        clean_db(post_conn, post_cur, "visitor")

    for x in range(len(visitor_list)):
        id = visitor_list[x].get('_id')

        query = "INSERT INTO visitor VALUES ( $${}$$) ON CONFLICT DO NOTHING".format(id)

        post_cur.execute(query)

def insert_product_data (post_conn, post_cur, product_list, clear = False):
    if clear:
        clean_db(post_conn, post_cur, "product")

    for x in range(len(product_list)):
        product_id = product_list[x].get("_id")

        selling_price = -1

        if "price" in product_list[x]:
            product_price = product_list[x].get("price")
            if "selling_price" in product_price:
                selling_price = product_price.get("selling_price")

        query = "INSERT  INTO product VALUES ( $${}$$, {} ) ON CONFLICT (_id) DO NOTHING".format(product_id, selling_price)

        post_cur.execute(query)

def insert_product_visitor_similars_data(post_conn, post_cur, visitor_list, clear = False):
    if clear:
        clean_db(post_conn, post_cur, "product_visitor_similars")

    for x in range(len(visitor_list)):
        visitor_id = visitor_list[x].get('_id')

        if "recommendations" in visitor_list[x]:
            visitor_recommendation_list = visitor_list[x].get('recommendations').get('similars')

            for y in range(len(visitor_recommendation_list)):
                product_id = visitor_recommendation_list[y]
                query = "INSERT INTO product_visitor_similars VALUES($${}$$, $${}$$)".format(product_id, visitor_id)
                post_cur.execute(query)

clean_db(post_conn, post_cur, "product_visitor_similars")
clean_db(post_conn, post_cur, "visitor")
clean_db(post_conn, post_cur, "product")

product_list = loadCollectionIntoList('products')
visitor_list = loadCollectionIntoList('visitors')

insert_product_data(post_conn, post_cur, product_list)
insert_visitor_data(post_conn, post_cur, visitor_list)
insert_product_visitor_similars_data(post_conn, post_cur, visitor_list)


post_conn.commit()
post_cur.close()
post_conn.close()
