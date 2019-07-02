from datetime import datetime
from postgres_functions import connectToPostgreSQL
from mongodb_functions import getProductsFromList


def insertPostgres(cur, values, tabel):
    sql = 'INSERT INTO ' + tabel + ' VALUES (' + values + ')'
    cur.execute(sql)


def getMostPurchasedProducts(cur, buids):
    product_list = []
    counter_list = []

    buids = str(buids).strip('[]')
    buids = buids.replace('\"', '')
    sql = 'SELECT orders FROM orders WHERE buid IN (' + buids + ')'
    cur.execute(sql)
    row = cur.fetchone()

    a = 0
    while row is not None:
        a += 1
        if row[0] not in product_list:
            product_list.append(row[0])
            counter_list.append(1)
        else:
            counter_list[product_list.index(row[0])] += 1
        row = cur.fetchone()

    x = 0
    topProd = []
    while x < 5:
        most_sold_id = product_list[counter_list.index(max(counter_list))]
        most_sold_count = max(counter_list)
        topProd.append(most_sold_id)
        counter_list.remove(most_sold_count)
        product_list.remove(most_sold_id)
        x += 1

    return topProd


def getBuidInThisTimeInterval(conn, cur, start_datum, end_datum):
    datum = start_datum
    dagenineenmaand = 32  # In code wordt 31 gebruikt
    maandenineenjaar = 13  # In code wordt 12 gebruikt
    dag = 1
    poproducten = []
    buids = []

    a = 1
    while dag != 0:
        sql = 'SELECT buids FROM sessions WHERE datum LIKE \'' + datum + '\''
        cur.execute(sql)

        row = cur.fetchone()
        datum = datum.split('-')
        if (row is None and (datum[2] == '29' or datum[2] == '30' or datum[2] == '31')):
            skip = 1
        else:
            skip = 0

        while row is not None:
            buids.append('\'' + row[0] + '\'')
            row = cur.fetchone()

        datum[2] = int(datum[2]) + 1
        if datum[2] == dagenineenmaand:
            datum[1] = int(datum[1]) + 1
            datum[2] = 1
        if datum[1] == maandenineenjaar:
            datum[0] = int(datum[0]) + 1
            datum[1] = 1
        if datum[2] in range(0, 10):
            datum[2] = str(0) + str(datum[2])
        if datum[1] in range(0, 10):
            datum[1] = str(0) + str(datum[1])
        datum = str(datum[0]) + '-' + str(datum[1]) + '-' + str(datum[2])
        if datum == end_datum:
            break
        if dag % 7 == 0 and skip == 0:
            poproducten.append(getMostPurchasedProducts(cur, buids))
            buids = []
            print(a)
            a = a + 1
        elif skip == 1:
            continue

        dag = dag + 1

    for nummer_van_een_week in range(len(poproducten)):
        for product in range(len(poproducten[nummer_van_een_week])):
            values = []
            values.append(nummer_van_een_week + 1)
            values.append(poproducten[nummer_van_een_week][product])
            values = str(values).strip('[]')
            values = values.replace('\"', '\'')
            insertPostgres(cur, values, 'topperweek')

    conn.commit()


def somvandagen(index,lst):
    som=0

    for i in range(index+1):
        som=lst[index]+som
        index=index-1

    return som


def weekvandaag():
    time=str(datetime.now())
    aantaldagenineenmaand=[31,28,31,30,31,30,31,31,30,31,30,31]

    time=time.split(' ')
    time=time[0].split('-')
    week=((somvandagen(int(time[1])-2,aantaldagenineenmaand)+int(time[2]))//7)+1

    return(week)


def getTopPerWeek(cur, week = weekvandaag()):
    topProd = []

    sql = 'SELECT product FROM topperweek WHERE week IN (' + str(week) + ')'
    cur.execute(sql)
    row = cur.fetchone()

    while row is not None:
        topProd.append(row[0])
        row = cur.fetchone()

    return (topProd)


def getMostPopularThisWeek():
    conn = connectToPostgreSQL()
    cur = conn.cursor()
    top_per_week = getTopPerWeek(cur)
    cur.close()
    conn.close()
    ret_list = getProductsFromList(top_per_week)
    return ret_list


def loadIntoDB():
    conn = connectToPostgreSQL()
    cur = conn.cursor()
    start_datum = '2018-01-01'
    end_datum = '2019-01-02'
    getBuidInThisTimeInterval(conn, cur, start_datum, end_datum)
    cur.close()
    conn.close()
