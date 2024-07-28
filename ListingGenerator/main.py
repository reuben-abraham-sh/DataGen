import constants
import utils


if __name__ == "__main__":        
    #res = get_sorted_manifest_tuple("manifest.txt")
    listing_id = utils.insert_qa_listing(4, 32.0, 22034, '510', 2042891, '1', '4')
    print("CREATED LISTING: ", listing_id)    