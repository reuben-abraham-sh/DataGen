QA_VGG_CONNECTION_STRING = "Driver={ODBC Driver 18 for SQL Server};Server=qa.viagogo.sql.viagogo.corp;Database=viagogo;Trusted_Connection=yes;TrustServerCertificate=yes; "
BIGGEST_SEAT_CHUNK_SIZE = 10

SEAT_LEVEL_LISTING_INSERT_QUERY_BULK = """SELECT NULL; INSERT INTO dbo.Listing (ListingTypeID, EventID, UserID, \
                         TicketLocationAddressID, GuaranteePaymentMethodID, \
                         SellerAffiliateID, AvailableTickets, \
                         OriginalAvailableTickets, SplitID, Section, SeatFrom, SeatTo, \
                         CurrencyCode, ListingStateID, IsConsignment, VersionStamp, \
                         ListingCreateDate, SellerZoneID, IsGeneralAdmission, DefaultCurrentPrice, ListingFeeClassID, SellerNetProceeds, \
                            TicketClassID, IsInHand, ETicketTypeId, ExpirationUpdateDate, IsPickupAvailable, ListingExpirationDate, FaceValue, \
                         FaceValueCurrencyCode, RowID, Row, ClientApplicationID, FraudStateID, SystemUser_Audit, ApplicationName_Audit, \
                        InternalHoldStateID, IsFromStubHub, IsPreUploaded) \
                        OUTPUT Inserted.ListingID
values \
    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

STANDING_ROW_LISTING_INSERT_QUERY_BULK = """SELECT NULL; INSERT INTO dbo.Listing (ListingTypeID, EventID, UserID, \
                         TicketLocationAddressID, GuaranteePaymentMethodID, \
                         SellerAffiliateID, AvailableTickets, \
                         OriginalAvailableTickets, SplitID, Section, \
                         CurrencyCode, ListingStateID, IsConsignment, VersionStamp, \
                         ListingCreateDate, SellerZoneID, IsGeneralAdmission, DefaultCurrentPrice, ListingFeeClassID, SellerNetProceeds, \
                            TicketClassID, IsInHand, ETicketTypeId, ExpirationUpdateDate, IsPickupAvailable, ListingExpirationDate, FaceValue, \
                         FaceValueCurrencyCode, RowID, Row, ClientApplicationID, FraudStateID, SystemUser_Audit, ApplicationName_Audit, \
                        InternalHoldStateID, IsFromStubHub, IsPreUploaded) \
                        OUTPUT Inserted.ListingID
values \
    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

LISTING_INSERT_QUERY = "SET NOCOUNT ON; INSERT INTO dbo.Listing (ListingTypeID, EventID, UserID, \
                         TicketLocationAddressID, GuaranteePaymentMethodID, \
                         SellerAffiliateID, AvailableTickets, \
                         OriginalAvailableTickets, SplitID, Section, SeatFrom, SeatTo, \
                         CurrencyCode, ListingStateID, IsConsignment, VersionStamp, \
                         ListingCreateDate, SellerZoneID, IsGeneralAdmission, DefaultCurrentPrice, ListingFeeClassID, SellerNetProceeds, \
                         TicketClassID, IsInHand, ETicketTypeId, ExpirationUpdateDate, IsPickupAvailable, ListingExpirationDate, FaceValue, \
                         FaceValueCurrencyCode, RowID, Row, ClientApplicationID, FraudStateID, SystemUser_Audit, ApplicationName_Audit, \
                        InternalHoldStateID, IsFromStubHub, IsPreUploaded) \
values \
    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); SELECT SCOPE_IDENTITY() AS ID;"

STANDING_ROW_LISTING_INSERT_QUERY = "SET NOCOUNT ON; INSERT INTO dbo.Listing (ListingTypeID, EventID, UserID, \
                         TicketLocationAddressID, GuaranteePaymentMethodID, \
                         SellerAffiliateID, AvailableTickets, \
                         OriginalAvailableTickets, SplitID, Section, \
                         CurrencyCode, ListingStateID, IsConsignment, VersionStamp, \
                         ListingCreateDate, SellerZoneID, IsGeneralAdmission, DefaultCurrentPrice, ListingFeeClassID, SellerNetProceeds, \
                            TicketClassID, IsInHand, ETicketTypeId, ExpirationUpdateDate, IsPickupAvailable, ListingExpirationDate, FaceValue, \
                         FaceValueCurrencyCode, RowID, Row, ClientApplicationID, FraudStateID, SystemUser_Audit, ApplicationName_Audit, \
                        InternalHoldStateID, IsFromStubHub, IsPreUploaded) \
values \
    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); SELECT SCOPE_IDENTITY() AS ID;"


LISTING_TYPE_ID = 1
EVENT_ID = 154249855
USER_ID = '1723E175-99D8-4680-BDB5-7E52F8EDEC7A'
TICKET_LOCATION_ADDRESS_ID = 72738
GUARANTEE_PAYMENT_METHOD_ID = 151620
SELLER_AFFILIATE_ID = 0
SPLIT_ID = 1
CURRENCY_CODE = 'USD'
LISTING_STATE_ID = 1
IS_CONSIGNMENT = 0
SELLER_ZONE_ID = 0
IS_GA = 0
LISTING_FEE_CLASS_ID = 4
IS_IN_HAND = 0
E_TICKET_TYPE_ID = 11
IS_PICKUP_AVAILABLE = 0
FACE_VALUE_CURRENCY_CODE = 'USD'
CLIENT_APPLICATION_ID = 3
FRAUD_STATE_ID = 3
SYSTEM_AUDIT = 'VIAGOGO\AppSupplyCmpl$'
APPLICATION_AUDIT = 'Viagogo Supply Compliance Service QA'
COMPLIANCE_BIT_MASK = '0xE7DEFFFF'
INTERNAL_HOLD_STATE_ID = 0
IS_FROM_SH = 0
# Adding a placeholder section since the mapping is done via the RowId on the listing
SECTION = '100'
IS_PREUPLOADED = 1

# For Section and Row information
CONFIG_IG = 581459
FETCH_SECTION_AND_ROW_NAMES = "SELECT sr.RowID, ctr.ContentBody as RowName, s.SectionID, cts.ContentBody as SectionName \
FROM Venue.ConfigSectionRow csr \
JOIN Venue.SectionRow sr on csr.RowID = sr.RowID \
JOIN dbo.ContentText ctr on ctr.ContentID = sr.NameContentID and (ctr.LCID = 2057 or ctr.LCID = 1033)\
JOIN Venue.Section s on sr.SectionID = s.SectionID \
JOIN dbo.ContentText cts on cts.ContentID = s.NameContentID and (cts.LCID = 2057 or cts.LCID = 1033) \
WHERE csr.ConfigID = {};"