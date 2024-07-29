import constants
import utils


if __name__ == "__main__":        
    #res = get_sorted_manifest_tuple("manifest.txt")
    #listing_id = utils.insert_single_listing(4, 32.0, 22034, 2042891, '1', '4')
    results = utils.bulk_insert_listing()
    print("RESULTS: ", results)
    #print(lst)
    #print("CREATED LISTING: ", listing_id)