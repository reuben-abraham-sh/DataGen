import constants
import utils
from collections import defaultdict

def batch_list(elements, batch_size=100):    
    for i in range(0, len(elements), batch_size):
        yield elements[i:i + batch_size]

if __name__ == "__main__":

    # remember to change the EVENTID in the constants file.
    #seat_lvl, standing_row_lvl = utils.get_sorted_manifest_tuple("manifest_padres.txt")

    # fetch section and row names
    row_names, section_names = utils.fetch_section_and_row_data()    

    #seat_lvl_param_list, standing_row_lvl_param_list = utils.generate_sql_param_list(seat_lvl, standing_row_lvl)
    #print(len(seat_lvl_param_list), len(standing_row_lvl_param_list))

    #listing_id = utils.insert_single_listing(3, 32.0, 4051, 2034256, None, None)
    # #print("ListingId ",listing_id)
    #utils.bulk_insert_listing(seat_lvl_param_list, standing_row_lvl_param_list)
    #seat_lvl_results, standing_row_results = utils.bulk_insert_listing(seat_lvl_param_list, standing_row_lvl_param_list)
    #print("RESULTS Seat LVL: ", seat_lvl_results)
    #print("RESULTS Standing Row: ", standing_row_results)
    