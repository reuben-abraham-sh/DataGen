--<< THIS FILE IS CONNECTED TO QA >>
use viagogo

-- State of Listing Active:1, Inactive:2, 4:Expired, 5:Fully Sold, 6:Deleted
select *
from viagogo.dbo.ListingState;

select *
from dbo.Event where EventId = 153763453;

select *
from viagogo.dbo.Listing where ListingId = 50151861390;

-- as far as I can tell, this dbo.ListingSectionMapping needs to be done as well.
select top 10 *
from viagogo.dbo.ListingSectionMapping;

select top 10 *
from viagogo.dbo.Seat;

----------- USER DETAIL ---------
select top 10 *
from viagogo.dbo.UserDetail where
                                --UserID = '1723E175-99D8-4680-BDB5-7E52F8EDEC7A'
                                FirstName = 'Reuben' and LastName = 'Abraham';
select top 10 *
from viagogo.dbo.Users;

-------
select *
from viagogo.dbo.Listing where ListingId = 50151861390;

/*
 fields to set:
 1. ListingTypeID: 1
 2. EventID: 152168498
 3. UserID: '93E29545-A45D-4667-81AF-0DFE82A4CA4C'
 4. TicketLocationAddressID: 72738
 5. GuaranteePaymentMethodID: 151620
 6. SellerAffiliateID: 0
 7. AvailableTickets: 2
 8. OriginalAvailableTickets: 2
 9. SplitID: 1
 10. Section: 510
 11. SeatFrom: 1
 12. SeatTo: 2
 13. CurrencyCode: USD
 14. ListingStateID: 1
 15. IsConsignment: 0
 16. VersionStamp: getutcdate()
 17. ListingCreationDate: getutcdate()
 */

insert into dbo.Listing (ListingTypeID, EventID, UserID,
                         TicketLocationAddressID, GuaranteePaymentMethodID,
                         SellerAffiliateID, AvailableTickets,
                         OriginalAvailableTickets, SplitID, Section, SeatFrom, SeatTo,
                         CurrencyCode, ListingStateID, IsConsignment, VersionStamp,
                         ListingCreateDate, SellerZoneID, IsGeneralAdmission, DefaultCurrentPrice, ListingFeeClassID, SellerNetProceeds,
                            TicketClassID, IsInHand, ETicketTypeId, ExpirationUpdateDate, IsPickupAvailable, ListingExpirationDate, FaceValue,
                         FaceValueCurrencyCode, RowID, ClientApplicationID, FraudStateID, SystemUser_Audit, ApplicationName_Audit, --ComplianceBitmask,
                        InternalHoldStateID, IsFromStubHub)
values
    (1, 152168498, '93E29545-A45D-4667-81AF-0DFE82A4CA4C', 72738, 151620, 0, 2, 2, 1, '510', '1', '2', 'USD', 1, 0,
     getutcdate(), getutcdate(), 0, 0, 12.00, 4, 11.34, 22034, 0, 11, '2024-10-25 17:52:25.06', 0, '2024-11-25 17:52:25.06', 18.324,
     'USD', 2042891, 3, 3, 'VIAGOGO\AppSupplyCmpl$', 'Viagogo Supply Compliance Service QA', --CONVERT(varbinary, '0xE7DEFFFF'),
 0, 0)


select *
from viagogo.dbo.Listing where EventID = 152168498;

select *
from viagogo.dbo.Address where AddressID = 72738