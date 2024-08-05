import constants
import db
import datetime
from tqdm import tqdm
from collections import defaultdict
import random

def get_sorted_manifest_tuple(filename):
    result = []
    unaccounted_counter = 0
    seat_lvl_counter = 0
    seat_lvl_dict = defaultdict(set)
    standing_rows = set()
    with open(filename) as file:        
        for line in tqdm(file):
            formatted_line_list = line.strip().split('_')
            if len(formatted_line_list) == 4:
                # seat level manifest entries
                seat = int(formatted_line_list[-1])
                key = "_".join(formatted_line_list[:-1])
                seat_lvl_dict[key].add(seat)
                seat_lvl_counter += 1
            elif len(formatted_line_list) == 3:
                # standing rows
                standing_row = "_".join(formatted_line_list)                
                standing_rows.add(standing_row)
            else:
                # standing sections come from here. - TBD extend program to capture.
                unaccounted_counter += 1

    print("Seat level counter: ", seat_lvl_counter)
    print("Standing row counter: ", len(standing_rows))
    print("Unaccounted for: ", unaccounted_counter)

    return seat_lvl_dict, standing_rows


def get_dates():
    now = datetime.datetime.now()    
    now_plus_six_m = now + datetime.timedelta(days = 90)
    return (now.strftime("%Y-%m-%d %H:%M:%S"), now_plus_six_m.strftime("%Y-%m-%d %H:%M:%S"))


def weighted_random_number(n):
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    weights = [1, 15, 32, 17, 5, 7, 4, 4, 3, 3]
    return random.choices(numbers[:n], weights=weights[:n], k=1)[0]


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
            chunk = weighted_random_number(min(constants.BIGGEST_SEAT_CHUNK_SIZE, total_seats_remaining))
            chunks.append((start, start+chunk-1))
            start = start + chunk
            total_seats_remaining -= chunk

    return chunks


def generate_sql_param_list(seat_lvl, standing_row_lvl, row_and_section_data):

    seat_result = []
    standing_row_result = []
    datetime_now, datetime_six_months = get_dates()
    row_section_metadata_keys = row_and_section_data.keys()
    rows_without_metadata, standing_rows_without_metadata = 0, 0
    
    # dealing with seat level    
    for key, seats in seat_lvl.items():        
        chunked_seats = chunk_seats(seats)
        if chunked_seats == None:
            print(f"Anomaly: Key:{key} -- Seats:{seats}")            

        key_split = key.split("_")
        ticketclass_id = int(key_split[0])
        row_id = int(key_split[-1])
        row_name, section_name = None, constants.SECTION #default values
        if row_id in row_section_metadata_keys:
            row_name, section_name = row_and_section_data[row_id]
        else:
            rows_without_metadata += 1            

        price = random.uniform(10, 50) # setting same price for all listings of this row for now

        for seat_from, seat_to in chunked_seats:

            available_tickets = seat_to - seat_from + 1
            seat_result.append((constants.LISTING_TYPE_ID, constants.EVENT_ID, constants.USER_ID,
                constants.TICKET_LOCATION_ADDRESS_ID, constants.GUARANTEE_PAYMENT_METHOD_ID, constants.SELLER_AFFILIATE_ID,
                available_tickets, available_tickets, constants.SPLIT_ID, section_name, str(seat_from), str(seat_to), constants.CURRENCY_CODE,
                constants.LISTING_STATE_ID, constants.IS_CONSIGNMENT, datetime_now, datetime_now, constants.SELLER_ZONE_ID, constants.IS_GA,
                price, constants.LISTING_FEE_CLASS_ID, price - 1, ticketclass_id, constants.IS_IN_HAND, constants.E_TICKET_TYPE_ID, datetime_six_months,
                constants.IS_PICKUP_AVAILABLE, datetime_six_months, 20.0, constants.FACE_VALUE_CURRENCY_CODE, row_id, row_name, constants.CLIENT_APPLICATION_ID,
                constants.FRAUD_STATE_ID, constants.SYSTEM_AUDIT, constants.APPLICATION_AUDIT, constants.INTERNAL_HOLD_STATE_ID, constants.IS_FROM_SH, constants.IS_PREUPLOADED
            ))     

    # dealing with standing row level
    for standing_row in standing_row_lvl:        
        # right now, just a single listing on standing row sections
        standing_row_split = standing_row.split("_")
        ticketclass_id = int(standing_row_split[0])
        row_id = int(standing_row_split[-1])
        row_name, section_name = None, constants.SECTION #default values
        if row_id in row_section_metadata_keys:
            row_name, section_name = row_and_section_data[row_id]
        else:
            standing_rows_without_metadata += 1

        price = random.uniform(10, 50) # setting same price for all listings of this row for now
        available_tickets = weighted_random_number(10)

        standing_row_result.append((constants.LISTING_TYPE_ID, constants.EVENT_ID, constants.USER_ID,
            constants.TICKET_LOCATION_ADDRESS_ID, constants.GUARANTEE_PAYMENT_METHOD_ID, constants.SELLER_AFFILIATE_ID,
            available_tickets, available_tickets, constants.SPLIT_ID, section_name, constants.CURRENCY_CODE,
            constants.LISTING_STATE_ID, constants.IS_CONSIGNMENT, datetime_now, datetime_now, constants.SELLER_ZONE_ID, constants.IS_GA,
            price, constants.LISTING_FEE_CLASS_ID, price - 1, ticketclass_id, constants.IS_IN_HAND, constants.E_TICKET_TYPE_ID, datetime_six_months,
            constants.IS_PICKUP_AVAILABLE, datetime_six_months, 20.0, constants.FACE_VALUE_CURRENCY_CODE, row_id, row_name, constants.CLIENT_APPLICATION_ID,
            constants.FRAUD_STATE_ID, constants.SYSTEM_AUDIT, constants.APPLICATION_AUDIT, constants.INTERNAL_HOLD_STATE_ID, constants.IS_FROM_SH, constants.IS_PREUPLOADED
        ))
        
    print("Rows without Row/Seat Names: ", rows_without_metadata)
    print("Standing Rows without Row/Seat Names: ", standing_rows_without_metadata)

    return seat_result, standing_row_result


def batch_params(elements, batch_size=250):
    for i in range(0, len(elements), batch_size):
        yield elements[i:i + batch_size]


def bulk_insert_listing(seat_lvl_param_list, standing_row_lvl_param_list):  
    total_seat_level_listing_ids = []
    batches = list(batch_params(seat_lvl_param_list))        

    for idx, batch in tqdm(enumerate(batches)):
        print(f"Running Batch {idx} : {len(batch)} Inserts")
        seat_lvl_results = db.bulk_insert_listing_helper(batch, constants.SEAT_LEVEL_LISTING_INSERT_QUERY_BULK)
        total_seat_level_listing_ids.extend(seat_lvl_results)

    # No need for batching here
    standing_row_results = db.bulk_insert_listing_helper(standing_row_lvl_param_list, constants.STANDING_ROW_LISTING_INSERT_QUERY_BULK)
    return total_seat_level_listing_ids, standing_row_results


def fetch_section_and_row_data():
    data = db.read_data(constants.FETCH_SECTION_AND_ROW_NAMES.format(constants.CONFIG_IG))
    if data == None:
        return None

    row_and_section_data = defaultdict()    

    for row_id, row_name, section_id, section_name in data:
        if row_name == "Not Specified":
            row_name = None

        row_and_section_data[row_id] = (row_name, section_name)        
        
    return row_and_section_data