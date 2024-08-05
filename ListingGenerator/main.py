import utils
import db

if __name__ == "__main__":

    # use to insert a single listing
    '''
    data = [(1391829,'1','CL1'),(1391833,'1','CL2'),(2089457,'1','STE202'),(2089460,'1','STE203'), \
    (2089463,'1','STE204'),(2089466,'1','STE205'),(2089469,'1','STE206'),(2089472,'1','STE207'),(2089475,'1','STE208'),(2089478,'1','STE209'), \
    (2089481,'1','STE210'),(2089484,'1','STE211'),(2089487,'1','STE212'),(2089490,'1','STE213'),(2089493,'1','STE214'),(2089496,'1','STE215'), \
    (2089499,'1','STE216'),(2089502,'1','STE217'),(2089505,'1','STE218'),(2089508,'1','STE219'),(2089511,'1','STE220'),(2089514,'1','STE221'), (2089517,'1','STE222'), \
    (2089520,'1','STE223'),(2089523,'1','STE224'),(2089526,'1','STE225'),(2089529,'1','STE226'),(2089532,'1','STE227'),(2089535,'1','STE228'),(2089538,'1','STE229'),(2089541,'1','STE230'), \
    (2089544,'1','STE231'),(2089547,'1','STE232'),(2089550,'1','STE233')]

    for row_id, row_name, section_name in data:
        listing_id = db.insert_single_listing(2, 32.0, 25275, row_id, '1',section_name, None, None)
        print("ListingId ",listing_id)
    '''

    # remember to change the EVENTID AND CONFIGID in the constants file.
    seat_lvl, standing_row_lvl = utils.get_sorted_manifest_tuple("./manifests/manifest_dodgers_155085969.txt")
    
    row_and_section_data = utils.fetch_section_and_row_data()

    seat_lvl_param_list, standing_row_lvl_param_list = utils.generate_sql_param_list(seat_lvl, standing_row_lvl, row_and_section_data)
     
    seat_lvl_results, standing_row_results = utils.bulk_insert_listing(seat_lvl_param_list, standing_row_lvl_param_list)
    
 