import pyodbc
import constants
import datetime

def get_sorted_manifest_tuple(filename):
    result = []
    with open(filename) as file:
        counter = 0
        for line in file:
            result.append(tuple([int(x) for x in line.strip().split('_')]))
            counter += 1
            if counter == 10:
                break
    return sorted(result)

def fetch_from_qa():
 
    cnxn = pyodbc.connect(constants.QA_VGG_CONNECTION_STRING)
    cursor = cnxn.cursor()

    cursor.execute("SELECT TOP 10 ListingID FROM dbo.Listing")
    row = cursor.fetchone()  
    while row:     
        print(row)      
        row = cursor.fetchone() 
    
    cursor.close()
    cnxn.close()


def get_dates():

    now = datetime.datetime.now()    
    now_plus_six_m = now + datetime.timedelta(days = 90)
    return (now.strftime("%Y-%m-%d %H:%M:%S"), now_plus_six_m.strftime("%Y-%m-%d %H:%M:%S"))

def generate_param_list():

    params = [(4, 32.0, 22034, 2042891, '1', '4'),(2, 24.0, 22034, 2042891, '5', '6'),(2, 24.0, 22034, 2042891, '7', '8')]
    result = []
    datetime_now, datetime_six_months = get_dates()

    for av_tix, price, tc, row, sf, st in params:
        result.append((constants.LISTING_TYPE_ID, constants.EVENT_ID, constants.USER_ID,
            constants.TICKET_LOCATION_ADDRESS_ID, constants.GUARANTEE_PAYMENT_METHOD_ID, constants.SELLER_AFFILIATE_ID,
            av_tix, av_tix, constants.SPLIT_ID, constants.SECTION, sf, st, constants.CURRENCY_CODE,
            constants.LISTING_STATE_ID, constants.IS_CONSIGNMENT, datetime_now, datetime_now, constants.SELLER_ZONE_ID, constants.IS_GA,
            price, constants.LISTING_FEE_CLASS_ID, price - 1, tc, constants.IS_IN_HAND, constants.E_TICKET_TYPE_ID, datetime_six_months,
            constants.IS_PICKUP_AVAILABLE, datetime_six_months, 20.0, constants.FACE_VALUE_CURRENCY_CODE, row, constants.CLIENT_APPLICATION_ID,
            constants.FRAUD_STATE_ID, constants.SYSTEM_AUDIT, constants.APPLICATION_AUDIT, constants.INTERNAL_HOLD_STATE_ID, constants.IS_FROM_SH, constants.IS_PREUPLOADED
        ))

    return result


def bulk_insert_listing():

    params = generate_param_list()
    try:
        cnxn = pyodbc.connect(constants.QA_VGG_CONNECTION_STRING)
        cursor = cnxn.cursor()  
        cursor.fast_executemany = True
        cursor.executemany(constants.LISTING_INSERT_QUERY_BULK, params)        

        results = []

        try:
            first_result = cursor.fetchall()
        except pyodbc.ProgrammingError:
            first_result = None        
        while cursor.nextset():
            results.append(cursor.fetchall()[0][0])                
                
        cnxn.commit()
        if not results or len(results) == 0:
            return None

        return results

    except Exception as e:
        print("Error:", e)
        cnxn.rollback()
        return None
    finally:
        cursor.close()
        cnxn.close() 


def insert_single_listing(available_tickets, price, ticket_class_id, row_id, seat_from, seat_to):
    try:
        datetime_now, datetime_six_months = get_dates()

        cnxn = pyodbc.connect(constants.QA_VGG_CONNECTION_STRING)
        cursor = cnxn.cursor()

        cursor.execute(constants.LISTING_INSERT_QUERY, (constants.LISTING_TYPE_ID, constants.EVENT_ID, constants.USER_ID,
            constants.TICKET_LOCATION_ADDRESS_ID, constants.GUARANTEE_PAYMENT_METHOD_ID, constants.SELLER_AFFILIATE_ID,
            available_tickets, available_tickets, constants.SPLIT_ID, constants.SECTION, seat_from, seat_to, constants.CURRENCY_CODE,
            constants.LISTING_STATE_ID, constants.IS_CONSIGNMENT, datetime_now, datetime_now, constants.SELLER_ZONE_ID, constants.IS_GA,
            price, constants.LISTING_FEE_CLASS_ID, price - 1, ticket_class_id, constants.IS_IN_HAND, constants.E_TICKET_TYPE_ID, datetime_six_months,
            constants.IS_PICKUP_AVAILABLE, datetime_six_months, 20.0, constants.FACE_VALUE_CURRENCY_CODE, row_id, constants.CLIENT_APPLICATION_ID,
            constants.FRAUD_STATE_ID, constants.SYSTEM_AUDIT, constants.APPLICATION_AUDIT, constants.INTERNAL_HOLD_STATE_ID, constants.IS_FROM_SH, constants.IS_PREUPLOADED
        ))
        
        inserted_id = cursor.fetchone()[0]  
        cnxn.commit()                     
        return inserted_id
    
    except Exception as e:
        print("Error:", e)
        cnxn.rollback()
        return None
    finally:
        cursor.close()
        cnxn.close() 