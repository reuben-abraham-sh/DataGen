import constants
import utils
from collections import defaultdict

def batch_list(elements, batch_size=100):    
    for i in range(0, len(elements), batch_size):
        yield elements[i:i + batch_size]

if __name__ == "__main__":

    # remember to change the EVENTID AND CONFIGID in the constants file.
    seat_lvl, standing_row_lvl = utils.get_sorted_manifest_tuple("manifest_yankees.txt")
    
    # fetch section and row names
    row_and_section_data = utils.fetch_section_and_row_data()

    seat_lvl_param_list, standing_row_lvl_param_list = utils.generate_sql_param_list(seat_lvl, standing_row_lvl, row_and_section_data)
    #print(seat_lvl_param_list[0], standing_row_lvl_param_list[0])

    #listing_id = utils.insert_single_listing(2, 32.0, 1745, 756346, None,'206','7', '8')
    #print("ListingId ",listing_id)    
    seat_lvl_results, standing_row_results = utils.bulk_insert_listing(seat_lvl_param_list, standing_row_lvl_param_list)
    #print("RESULTS Seat LVL: ", seat_lvl_results)
    #print("RESULTS Standing Row: ", standing_row_results)
 