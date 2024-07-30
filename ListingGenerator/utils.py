import pyodbc
import constants
import datetime
from tqdm import tqdm
from collections import defaultdict
import random

def get_sorted_manifest_tuple(filename):
    result = []
    non_seat_lvl_counter = 0
    hash_dict = defaultdict(set)
    with open(filename) as file:
        counter = 0
        for line in tqdm(file):
            formatted_line_list = line.strip().split('_')
            if len(formatted_line_list) == 4:
                # seat level manifest entries
                seat = int(formatted_line_list[-1])
                key = "_".join(formatted_line_list[:-1])
                hash_dict[key].add(seat)
                counter += 1
            else:
                non_seat_lvl_counter += 1 # instead, log it in another file.

    print("Seat level counter: ", counter)
    print("Non seat level counter", non_seat_lvl_counter)

    return hash_dict

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


def weighted_random_choice(n):
    weights = [1/(i+1) for i in range(n)]
    total = sum(weights)
    probabilities = [w / total for w in weights]
    return random.choices(range(1, n+1), probabilities)[0]


def group_continuous_numbers(sorted_seats):
    result = []
    current_group = [sorted_seats[0]]

    for i in range(1, len(sorted_seats)):
        if sorted_seats[i] == sorted_seats[i - 1] + 1:
            current_group.append(sorted_seats[i])
        else:
            result.append(current_group)
            current_group = [sorted_seats[i]]

    result.append(current_group)
    return result


def chunk_seats(seats):    
    chunks = []
    sorted_seats = sorted(seats)    
    groups = group_continuous_numbers(sorted_seats)

    for group in groups:

        start, end = group[0], group[-1]
        if start < 0 or len(group) != (end - start + 1):
            return None
        
        total_seats_remaining = len(group)

        while total_seats_remaining > 0:
            chunk = weighted_random_choice(min(constants.BIGGEST_SEAT_CHUNK_SIZE, total_seats_remaining))
            chunks.append((start, start+chunk-1))
            start = start + chunk
            total_seats_remaining -= chunk

    return chunks


def generate_sql_param_list(parsed_data):

    result = []
    datetime_now, datetime_six_months = get_dates()    
    for key, seats in parsed_data.items():
                
        chunked_seats = chunk_seats(seats)
        if chunked_seats == None:
            print(f"Anomaly: Key:{key} -- Seats:{seats}")
        
        print(f"Key:{key} \nSeats:{seats} \nChunks:{chunked_seats}")
        print("\n")               

    '''
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
    '''


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