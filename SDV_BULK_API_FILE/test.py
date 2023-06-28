import pandas as pd
import numpy as np
#from datetime import datetime
import datetime
import pyodbc
data = {

    "HeaderInfo": {
        "ProcessAreaId": "ENG",
        "DataSetName": "TEST_ENG4",
        "TargetSys": "SDD070",
        "NumOfRecords": 14,
        "Created_By": "T_WIP_USER5",
        "Created_On": "12/6/2023",
        "Changed_On": "27/6/2023",
        "Changed_By": " K kumar",
        "Status": "First Status",
        "Stage": "First Stage",

        "CountryKey": "CAN-US"
    },
    "InputSet": [
        {
            "FieldName": "PBUKR",
            "FieldDesc": "Entity",
            "FieldValue": 2200
        },
        {
            "FieldName": "DR",
            "FieldDesc": "DefaultRecords",
            "FieldValue": 0
        },
        {
            "FieldName": "PLFEZ",
            "FieldDesc": "Start Date",
            "FieldValue": "2023-06-03"
        },
        {
            "FieldName": "PLSEZ",
            "FieldDesc": "End Date",
            "FieldValue": "2026-06-08"
        },
        {
            "FieldName": "PST1",
            "FieldDesc": "POST1",
            "FieldValue": "Hello"
        },
        {
            "FieldName": "MANDT",
            "FieldDesc": "MANDT",
            "FieldValue": "30"
        },
        {
            "FieldName": "ZZ_CLIENT",
            "FieldDesc": "Client",
            "FieldValue": 1100016
        },
        {
            "FieldName": "ZZ_CLIENT",
            "FieldDesc": "Client",
            "FieldValue": 1100016
        },
        {
            "FieldName": "Email",
            "FieldDesc": "Requester E-Mail",
            "FieldValue": "kumar.andala@gmail.com"
        },
        {
            "FieldName": "PRART",
            "FieldDesc": "Engagement Type",
            "FieldValue": 1
        },
        {
            "FieldName": "Z3",
            "FieldDesc": "Eng Partner",
            "FieldValue": 3126673
        },
        {
            "FieldName": "Z4",
            "FieldDesc": "Eng Manager",
            "FieldValue": 3154886
        },
        {
            "FieldName": "L2_levels",
            "FieldDesc": "NoofL2_levels",
            "FieldValue": 2
        },
        {
            "FieldName": "M",
            "FieldDesc": "Material (L2)",
            "FieldValue": "6110-1107"
        },
        {
            "FieldName": "MO",
            "FieldDesc": "Market Offering (L2)",
            "FieldValue": "AE17063724A0956016"
        }
    ]
}


conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Users\pavankumar4\Documents\Database1.accdb;'
conn = pyodbc.connect(conn_str)
crsr = conn.cursor()
table_name = "DataSet_Input"
temp_df= pd.DataFrame([])
header = data['HeaderInfo']
body = data["InputSet"]
new_df = pd.DataFrame().from_records(body)
new_df.drop('FieldDesc',axis=1, inplace=True)
dictionary_df = new_df.to_dict(orient='index')
dictionary_df2 = new_df.to_dict()
table_name = 'DataSet_Input'
columns = crsr.columns(table=table_name)
for column in columns:
    column_name = column.column_name
    print('col names', column_name)

print('df', dictionary_df)
print(dictionary_df2)



conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Users\pavankumar4\Documents\Database1.accdb;'
conn = pyodbc.connect(conn_str)
crsr = conn.cursor()

table_name = "DataSet"
DatasetUID = 'TEST_ENGSYN379826'
condition_column = 'DataSet_GUID'

select_query = f"SELECT * from {table_name} WHERE {condition_column} = '{DatasetUID}'"

df = pd.read_sql_query(select_query, conn)

status_info = df['Status'].squeeze()


table_name1= 'DB_Status'
col_name1= 'DB_Status'
select_query1 = f"SELECT * from {table_name1} WHERE {col_name1} = '{status_info}'"
df2 = pd.read_sql_query(select_query1, conn)
Status_id = df2.loc[0, 'DB_Status_ID']
# df2= df2.item()
df['statusID']=int(Status_id)
print(df.to_json(orient='records'))


# Close the connection
conn.close()


def Fetch_Date_Timestamps():
    conn_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Users\pavankumar4\Documents\Database1.accdb;'
    conn = pyodbc.connect(conn_string)

    cursor = conn.cursor()
    sql_query = "SELECT Created_On FROM Dataset"

    # Execute the SQL query and fetch the results

    cursor.execute(sql_query)
    rows = cursor.fetchall()

    for row in rows:
        created_on = row.Created_On
        date = created_on.split('T')[0]
        formatted_date = date[5:7] + date[8:10] + date[0:4]  # Rearrange the date in MMDDYYYY format
        print(formatted_date)

    # Extract the dates from the timestamps
    # dates = [datetime.strptime(row.Created_On, "%Y-%m-%dT%H:%M:%S.%f").date() for row in results]

    # Close the database connection
    cursor.close()
    conn.close()






Fetch_Date_Timestamps()