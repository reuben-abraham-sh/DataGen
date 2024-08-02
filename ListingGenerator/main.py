import utils

if __name__ == "__main__":

    # use to insert a single listing
    #listing_id = utils.insert_single_listing(2, 32.0, 1745, 756346, None,'206','7', '8')
    #print("ListingId ",listing_id)   

    # remember to change the EVENTID AND CONFIGID in the constants file.
    seat_lvl, standing_row_lvl = utils.get_sorted_manifest_tuple("./manifests/manifest_padres.txt")
    
    row_and_section_data = utils.fetch_section_and_row_data()

    seat_lvl_param_list, standing_row_lvl_param_list = utils.generate_sql_param_list(seat_lvl, standing_row_lvl, row_and_section_data)
     
    seat_lvl_results, standing_row_results = utils.bulk_insert_listing(seat_lvl_param_list, standing_row_lvl_param_list)
    
 