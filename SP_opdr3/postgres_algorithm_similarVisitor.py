import random
from postgres_functions import connectToPostgreSQL, getProfile
from mongodb_functions import getProductsFromList


def getMostSimilarVisitors_order_based(visitor, visitor_previously_ordered):
    ret_list = []
    buid_similar_list = []
    buid_list = []
    buid_counter_list = []

    conn = connectToPostgreSQL()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    row = cur.fetchone()

    while row is not None:
        if row[0] not in visitor["buids"] and row[1] in visitor_previously_ordered and row[1] != "None":
            if row[0] not in buid_list:
                buid_list.append(row[0])
                buid_counter_list.append(1)
            else:
                buid_counter_list[buid_list.index(row[0])] += 1

        row = cur.fetchone()

    x = 0

    while x < 5:
        most_similar_buid = buid_list[buid_counter_list.index(max(buid_counter_list))]
        most_similar_buid_count = max(buid_counter_list)

        buid_similar_list.append(most_similar_buid)

        buid_counter_list.remove(most_similar_buid_count)
        buid_list.remove(most_similar_buid)

        x += 1

    cur.execute("SELECT * FROM visitors_buid")
    row = cur.fetchone()

    while row is not None:
        if row[1] in buid_similar_list:
            ret_list.append(row[0])

        row = cur.fetchone()

    cur.close()
    conn.close()
    return ret_list


def recommendProductsFromSimilarProfile(visitor_profile, similar_profile, parent_ret_list_size):
    ret_list = []
    temp_list = []

    for x in range(len(similar_profile['orders'])):
        for y in range(len(similar_profile['orders'][x])):
            if similar_profile['orders'][x][y] in visitor_profile["viewed_before"]:
                ret_list.append(similar_profile['orders'][x][y])
            else:
                temp_list.append(similar_profile['orders'][x][y])

    random.shuffle(temp_list)

    x = 0

    while len(ret_list) + parent_ret_list_size <= 10:
        if temp_list[x + 1] is None:
            break
        ret_list.append(temp_list[x])
        x += 1

    return ret_list

#parent function for algoritm. The return is display ready for the front-end. Takes data from the front-end as parameter
def getRecommendationFromSimilarVisitors(data):
    ret_list = []
    visitor_id = data.get("visitorId")
    visitor_profile = getProfile(visitor_id)
    visitor_previously_ordered = []
    similar_visitors_profiles = []

    if not visitor_profile["buids"]:
        return "ERROR - VISITOR NOT FOUND"

    #prepare a list of items the visitor has ordered before so it can be more easily checked later
    for x in range(len(visitor_profile["orders"])):
        for y in range(len(visitor_profile["orders"][x])):
            visitor_previously_ordered.append(visitor_profile["orders"][x][y])


    #find most similar visitors and prepare their profiles
    similar_visitors_id_list = getMostSimilarVisitors_order_based(visitor_profile, visitor_previously_ordered)

    for x in range(len(similar_visitors_id_list)):
        similar_visitors_profiles.append(getProfile(similar_visitors_id_list[x]))

    #keep fetching recommendable products based on the similar visitors until 10 items have been reached or the similar visitor list is exhausted
    x = 0
    while len(ret_list) <= 10:
        ret_list += recommendProductsFromSimilarProfile(visitor_profile, similar_visitors_profiles[x], len(ret_list))
        if x + 1 >= len(similar_visitors_profiles):
            break
        x += 1

    #prepare the list of product ids for display on the front-end
    return getProductsFromList(ret_list)
