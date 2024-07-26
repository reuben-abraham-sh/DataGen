

import pyodbc 

def get_sorted_manifest_tuple(filename):
    result = []
    with open(filename) as file:
        counter = 0
        for line in file:
            result.append(tuple([int(x) for x in line.strip().split('_')]))
            counter += 1
            if counter == 10:
                break
    return sorted(result)

def fetch_from_qa():
    conn_string = """ 
Driver={ODBC Driver 18 for SQL Server};Server=qa.viagogo.sql.viagogo.corp;Database=viagogo;Trusted_Connection=yes;TrustServerCertificate=yes; 
"""  
    print(conn_string)
    cnxn = pyodbc.connect(conn_string)  
    cursor = cnxn.cursor()

    cursor.execute("SELECT TOP 100 ListingID FROM dbo.Listing")
    row = cursor.fetchone()  
    while row:     
        print(row)      
        row = cursor.fetchone() 
    
    cursor.close()
    cnxn.close()	

if __name__ == "__main__":        
    #res = get_sorted_manifest_tuple("manifest.txt")
    #print(pyodbc.drivers())
    fetch_from_qa()
    #print(res)