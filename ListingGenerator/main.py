import constants
import utils
from collections import defaultdict


if __name__ == "__main__":
    
    # remember to change the EVENTID in the constants file.
    seat_lvl, standing_row_lvl = utils.get_sorted_manifest_tuple("manifest_yankees.txt")    
    seat_lvl_param_list, standing_row_lvl_param_list = utils.generate_sql_param_list(seat_lvl, standing_row_lvl)
    print(standing_row_lvl_param_list[0])

    # listing_id = utils.insert_single_listing(10, 32.0, 4109, 701325, None, None)
    # print("ListingId ",listing_id)
    # #results = utils.bulk_insert_listing(params_list)
    # print("RESULTS: ", results)
    