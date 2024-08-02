import pyodbc
import constants
import utils

def read_data(query):
    try:        
        conn = pyodbc.connect(constants.QA_VGG_CONNECTION_STRING)
        cursor = conn.cursor()            
        cursor.execute(query)
        data = cursor.fetchall()    
        return data
    except Exception as e:
        print("Error:", e)
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def insert_single_listing(available_tickets, price, ticket_class_id, row_id, row_name, section_name, seat_from, seat_to):
    try:
        datetime_now, datetime_six_months = utils.get_dates()

        cnxn = pyodbc.connect(constants.QA_VGG_CONNECTION_STRING)
        cursor = cnxn.cursor()

        if seat_from == None and seat_to == None:
            # standing row
            cursor.execute(constants.STANDING_ROW_LISTING_INSERT_QUERY, (constants.LISTING_TYPE_ID, constants.EVENT_ID, constants.USER_ID,
                constants.TICKET_LOCATION_ADDRESS_ID, constants.GUARANTEE_PAYMENT_METHOD_ID, constants.SELLER_AFFILIATE_ID,
                available_tickets, available_tickets, constants.SPLIT_ID, section_name, constants.CURRENCY_CODE,
                constants.LISTING_STATE_ID, constants.IS_CONSIGNMENT, datetime_now, datetime_now, constants.SELLER_ZONE_ID, constants.IS_GA,
                price, constants.LISTING_FEE_CLASS_ID, price - 1, ticket_class_id, constants.IS_IN_HAND, constants.E_TICKET_TYPE_ID, datetime_six_months,
                constants.IS_PICKUP_AVAILABLE, datetime_six_months, 20.0, constants.FACE_VALUE_CURRENCY_CODE, row_id, row_name, constants.CLIENT_APPLICATION_ID,
                constants.FRAUD_STATE_ID, constants.SYSTEM_AUDIT, constants.APPLICATION_AUDIT, constants.INTERNAL_HOLD_STATE_ID, constants.IS_FROM_SH, constants.IS_PREUPLOADED
            ))
        else:
            # regular listing
            cursor.execute(constants.LISTING_INSERT_QUERY, (constants.LISTING_TYPE_ID, constants.EVENT_ID, constants.USER_ID,
                constants.TICKET_LOCATION_ADDRESS_ID, constants.GUARANTEE_PAYMENT_METHOD_ID, constants.SELLER_AFFILIATE_ID,
                available_tickets, available_tickets, constants.SPLIT_ID, section_name, seat_from, seat_to, constants.CURRENCY_CODE,
                constants.LISTING_STATE_ID, constants.IS_CONSIGNMENT, datetime_now, datetime_now, constants.SELLER_ZONE_ID, constants.IS_GA,
                price, constants.LISTING_FEE_CLASS_ID, price - 1, ticket_class_id, constants.IS_IN_HAND, constants.E_TICKET_TYPE_ID, datetime_six_months,
                constants.IS_PICKUP_AVAILABLE, datetime_six_months, 20.0, constants.FACE_VALUE_CURRENCY_CODE, row_id, row_name, constants.CLIENT_APPLICATION_ID,
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


def bulk_insert_listing_helper(params, query):
    
    if params == None or len(params) == 0:
        return []

    try:
        cnxn = pyodbc.connect(constants.QA_VGG_CONNECTION_STRING)
        cursor = cnxn.cursor()  
        cursor.fast_executemany = True
        cursor.executemany(query, params)        

        results = []

        try:
            first_result = cursor.fetchall()
        except pyodbc.ProgrammingError:
            first_result = None        
        while cursor.nextset():
            insert_id = cursor.fetchall()[0][0]
            if insert_id != None:
                results.append(insert_id)               
                
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