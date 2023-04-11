
# AWS Access Key ID
MWS_ACCESS_KEY = 'AKIAXXXXXXXXXXXXXXXXXXXBGW2Q'
# Secret key:
MWS_SECRET_KEY = 'AYRbKFNrXXXXXXXXXXXXXXXXXXXXchgVlelLeDCQsWvsrdzI'
# MWS developer ID
MWS_DEV_ID = '1621111111111111111067'
# Seller ID
AMZ_SELLER_ID = 'A3XXXXXXXXXXXXXXXXXXXU02W3'

import datetime as dt
import mws
# from mws import Orders, Marketplaces

marketid_jp = 'A1XXXXXXXXXXXXXXX28'

import pickle
adresses = []

def get_inventory():
    inventory = mws.Products(MWS_ACCESS_KEY,MWS_SECRET_KEY,AMZ_SELLER_ID,region='JP')
    products = inventory.list_matching_products(marketid_jp,'Espinet','Grocery')
    for p in products.parsed.Products['Product']:
        print(p)
    return

def get_orders():

    orders_api = mws.Orders(MWS_ACCESS_KEY,MWS_SECRET_KEY,AMZ_SELLER_ID,region='JP')
    try:
        # orders = orders_api.list_orders(marketid_jp, orderstatus=('Unshipped'), max_results="100")
        date = dt.date.today() - dt.timedelta(7)
        orders = orders_api.list_orders(marketid_jp
                , orderstatus='Unshipped'
                ,created_after=date )
                # ,created_before=dt.datetime.today() )
        # orders = orders_api.list_orders(marketid_jp, created_after=None, created_before=None, lastupdatedafter=None, lastupdatedbefore=None, orderstatus=(), fulfillment_channels=(), payment_methods=(), buyer_email=None, seller_orderid=None, max_results="100", next_token=None)
    except:
        print('error')
    i = 0
    for order in orders.parsed.Orders['Order']:
        i += 1
        orders_amz = ''
        OrderStatus = order['OrderStatus']
        if OrderStatus == 'Shipped':
            continue
        elif OrderStatus != 'Unshipped':
            print('OrderStatus ', OrderStatus)
        
        print('order # ', i, order['OrderStatus'], ' :\n ') # , order , '\n')
        if 'ShippingAddress' in order:
            address = order['ShippingAddress']
        else:
            print('no ShippingAddress')
            continue
        # name = address.getvalue('Name')
        name = address['Name']
        # print(len(name))
        if ( ' ' in name ):
            n = name.split(' ')
            nom = n[0]
            prenom = n[1]  
        elif ( '　' in name ):
            n = name.split('　')
            nom = n[0]
            prenom = n[1]
            name = name.replace('　', ' ')
        else:
            nom = name[0:2]
            prenom = name[2:len(name)]

        zip = address['PostalCode']
        if (zip.find('-') == -1 ):
            zip_code = zip
        else:
            zip_code = zip.replace('-','')

        phone = address['Phone']
        if (phone.find('-') == -1 ):
            telephone = phone
        else:
            telephone = phone.replace('-','')
        
        StateOrRegion = address['StateOrRegion']
        AddressLine1 = address['AddressLine1']
        if 'AddressLine2' in address:
            AddressLine2 = address['AddressLine2']
        else:
            # AddressLine2 is None:
            AddressLine2 = ''
        
        if 'AddressLine3' in address:
            AddressLine3 = address['AddressLine3']
        else:
            # if AddressLine3 is None:
            AddressLine3 = ''

        if 'AddressLine4' in address:
            print('ddressLine4')

        # orders_amz = name + "," + nom + "," + prenom + "," 
        orders_amz = nom + " " + prenom + "," + nom + "," + prenom + "," 
        orders_amz += telephone + "," 
        orders_amz += zip_code + ","
        orders_amz += StateOrRegion + "," + AddressLine1 + "," + AddressLine2 + "," + AddressLine3 + ","
        orders_amz += "時間未指定,,YMT_compact,,,"
        print(orders_amz)
        adresses.append(orders_amz)
        AmazonOrderId = order['AmazonOrderId']
        print('AmazonOrderId  ', AmazonOrderId)
        # # shipping_details = orders_api.list_order_items(AmazonOrderId)
        # shipping_details = orders_api.get_order(AmazonOrderId)
        # print(shipping_details.parsed)
        # o = orders_api.get_order(AmazonOrderId)
        # print(o.parsed)

    saveAddresses()
    
    return

def saveAddresses():
    global adresses
    f = open(r'./orders_list_YMT.txt','w',encoding='utf-8') 
    for s in adresses:
        f.write("%s\n" % s)
    f.close()
    return

if __name__ == '__main__':
    get_orders()
    # get_inventory()