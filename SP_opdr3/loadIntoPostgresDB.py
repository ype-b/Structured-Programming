import pymongo
import psycopg2


def check(inhoud,cur):
    products = dict(inhoud[0])
    a=0
    b=0
    pos=[]

    if 'buids' not in products or len(products['buids'])==0:
        a=1
    if 'recommendations' not in products or 'viewed_before'not in products['recommendations'] or len(products['recommendations']['viewed_before'])==0:
        b=1
    if a!=1:
        Len=len(products['buids'])
        for i in range(len(products['buids'])):
            cur.execute('SELECT buids FROM sessions WHERE buids LIKE ' + '\'' + str(products['buids'][i]) + '\'' + ';')
            row= cur.fetchone()
            if row==None:
                Len=Len-1
                continue
            else:
                 pos.append(i)
        if Len==0:
            pos.append('None')
            a=1

    c=a+b

    if c==2:
        return(0)
    else:
        return(pos)


def visitor_buids_values(inhoud,colomen,pos):
    values = []
    products = dict(inhoud[0])

    for i in range(len(colomen)):
        if 'buids' in colomen[i]:
            for a in range(len(pos)):
                if pos[0] == 'None':
                    values.append(pos[0])
                else:
                    values.append(products[colomen[i]][pos[a]])
        else:
            values.append(str(products[colomen[i]]))

    return(values,len(pos))


def viewedbefore_values(inhoud,colomen):
    values = []
    products = dict(inhoud[0])

    if 'recommendations' not in products:
        products['recommendations']={'viewed_before':[]}
    if 'viewed_before'not in products['recommendations']:
        products['recommendations']={'viewed_before':[]}
    if len(products['recommendations']['viewed_before'])==0:
        products['recommendations']['viewed_before'].append('None')

    for i in range(len(colomen)):
        if colomen[i]=='viewed_before':
            for a in range(len(products['recommendations'][colomen[i]])):
                values.append(products['recommendations'][colomen[i]][a])
        else:
            values.append(str(products[colomen[i]]))

    return([values,len(products['recommendations']['viewed_before'])])


def visitors_values(inhoud,colomen):
    product = dict(inhoud[0])
    values=[str(product[colomen[0]])]

    return([values,1])


def orders_values(inhoud,colomen):
    values=[]
    products=dict(inhoud[0])

    if 'order' not in products or 'buid' not in products:
        return(0)
    if 'products' not in products['order']:
        return(0)
    if len(products['order']['products']) == 0:
        return (0)

    for a in range(len(colomen)):
        if type(products[colomen[a]]) == type(None):
            products[colomen[a]] = 'None'

        if colomen[a]=='buid':
            if type(products[colomen[a]][0]) == list:
                values.append(products[colomen[a]][0][0])
            else:
                values.append(products[colomen[a]][0])

        elif colomen[a]=='order':
            for i in range(len(products[colomen[a]]['products'])):
                values.append(products[colomen[a]]['products'][i]['id'])
        else:
            pass

    return([values,len(products['order']['products'])])


def sessions_values(inhoud,colomen):
    product = dict(inhoud[0])
    values=[]
    keys=product.keys()

    for i in range(len(colomen)):
        if colomen[i] not in keys:
             product[colomen[i]] = 'data is missing'

        if type(product[colomen[i]]) == type(None):
            product[colomen[i]] = 'None'

        if 'buid' in colomen[i]:
            if type(product[colomen[i]][0]) == list:
                values.append(product[colomen[i]][0][0])
            else:
                values.append(product[colomen[i]][0])
        elif 'session_start' in colomen[i]:
            a = str(product[colomen[i]])
            a = a.split(' ')
            values.append(a[0])
        else:
            values.append(product[colomen[i]])

    return([values,1])


def property_values(inhoud,colomen):
    product = dict(inhoud[0])
    values=[]
    key = product['properties'].keys()

    for i in range(len(colomen)):
        if colomen[i] == '_id':
            if '\'' in product[colomen[i]]:
                values.append(product[colomen[i]].replace('\'', ''))
            else:
                values.append(product[colomen[i]])
        else:
            if colomen[i] not in key:
                product['properties'][colomen[i]] = 'data is missing'
            if type(product['properties'][colomen[i]]) == type(None):
                product['properties'][colomen[i]] = 'None'
            if '\"' in product['properties'][colomen[i]]:
                values.append(product['properties'][colomen[i]].replace('\"', ''))
            elif '\'' in product['properties'][colomen[i]]:
                values.append(product['properties'][colomen[i]].replace('\'', ''))
            else:
                values.append(product['properties'][colomen[i]])

    return([values,1])


def product_values(inhoud,colomen):
    values=[]
    product=dict(inhoud[0])
    keys = product.keys()

    if 'category' not in keys:
        product['category'] = 'data is missing'
    if type(product['category']) == list:
        product['sub_category'] = product['category'][1]
        product['sub_sub_category'] = product['category'][2]
        product['category'] = product['category'][0]

    for i in range(len(colomen)):
        if colomen[i] not in keys:
            product[colomen[i]] = 'data is missing'

        if type(product[colomen[i]]) == type(None):
            product[colomen[i]] = 'None'

        if colomen[i] == 'price':
            if product[colomen[i]] =='data is missing':
                return(0)
            else:
                if product[colomen[i]]['selling_price']==0:
                    return(0)
                else:
                    values.append(product[colomen[i]]['selling_price'])
        elif colomen[i]== 'herhaalaankopen':
            values.append(str(product[colomen[i]]))
        else:
            if '\'' in product[colomen[i]]:
                values.append(product[colomen[i]].replace('\'', ''))
            else:
                values.append(product[colomen[i]])

    return([values,1])


def tabel_all_values(client, conn, cur, cur2, cur3):
    colomen = [['_id','brand','category','sub_category','sub_sub_category','gender','herhaalaankopen','price'],
               ['_id','bundel_sku','doelgroep','factor','gebruik','geschiktvoor','geursoort','huidconditie','huidtype','huidtypegezicht','inhoud','kleur','leeftijd','soort','soorthaarverzorging','soortmondverzorging','sterkte','type','typehaarkleuring','typetandenborstel','variant','waterproof'],
               ['buid','has_sale','session_start'],
               ['buid','order'],
               ['_id'],
               ['_id','viewed_before'],
               ['_id','buids']]

    table = ['product','sessions','visitors']
    l=1
    p=1
    e=1

    for a in range(1):
        a=1
        if table[a]=='product':
            collection = client['_opop_db'].products
            secondtabel='properties'
            thirdtabel =''
        elif table[a]=='sessions':
            collection = client['_opop_db'].sessions
            secondtabel='orders'
            thirdtabel = ''
        else:
            collection = client['_opop_db'].visitors
            secondtabel='viewed_before'
            thirdtabel='visitors_buid'
        for product in collection.find():
            tabel = table[a]
            inhoud =[]
            inhoud.append(product)
            if tabel=='product':
                tempvalues=[product_values(inhoud,colomen[0])]
                if tempvalues[0] != 0:
                    tempvalues.append(property_values(inhoud, colomen[1]))
            elif tabel=='sessions':
                tempvalues=[sessions_values(inhoud,colomen[2])]
                if tempvalues[0] != 0:
                    tempvalues.append(orders_values(inhoud, colomen[3]))
            elif tabel=='visitors':
                tempvalues = [check(inhoud, cur)]
                if tempvalues[0] != 0:
                    pos=tempvalues[0]
                    tempvalues=[]
                    tempvalues.append(visitors_values(inhoud, colomen[4]))
                    tempvalues.append(viewedbefore_values(inhoud, colomen[5]))
                    tempvalues.append(visitor_buids_values(inhoud,colomen[6],pos))

            l = l + 1

            if len(tempvalues)==1:
                if tempvalues[0]==0:
                    continue
            else:
                if tempvalues[1]==0:
                    continue

            e=e+1

            for c in range(len(tempvalues)):
                for i in range(tempvalues[c][1]):
                    if tempvalues[c][1] > 1:
                        values = str(tempvalues[c][0][i+1])
                        values =str([tempvalues[c][0][0],values])
                    else:
                        values = str(tempvalues[c][0])
                    values = values.strip('[]')
                    values = values.replace('\"', '\'')
                    p=insert(cur3, conn, values, tabel)+p
                if c==0:
                    tabel=secondtabel
                if c==1:
                    tabel=thirdtabel

    conn.commit()


def insert(cur3, conn, values,tabel):
    try:
        sql = 'INSERT INTO ' + tabel + ' VALUES (' + values + ')'
        cur3.execute(sql)

        if tabel=='sessions' or tabel == 'orders':
           conn.commit()
        return(0)
    except psycopg2.IntegrityError:
        conn.commit()
        return(1)


def databases():
    client = pymongo.MongoClient()
    conn = psycopg2.connect("dbname=AAIproject user=postgres password=pw")
    cur = conn.cursor()
    cur2 = conn.cursor()
    cur3= conn.cursor()
    tabel_all_values(client, conn, cur, cur2, cur3)
    conn.commit()
    cur.close()
    conn.close()

databases()