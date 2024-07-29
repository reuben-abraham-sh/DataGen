import constants
import utils
from collections import defaultdict


if __name__ == "__main__":
    
    parsed_data = utils.get_sorted_manifest_tuple("manifest.txt")
    params_list = utils.generate_sql_param_list(parsed_data)
    #listing_id = utils.insert_single_listing(4, 32.0, 22034, 2042891, '1', '4')
    #results = utils.bulk_insert_listing()
    #print("RESULTS: ", results)
    