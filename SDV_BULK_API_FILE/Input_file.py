from SDV_BULK_API_FILE.SDV_BULK_UPDATED_file_API import Bulk_Driver


header = {

"ProcessAreaId": "ENG",

"DataSetName": "TEST_ENG",

"TargetSys": "SDD070",

"CountryKey": "US",

"NumOfRecords": 55

}


body_list = [

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

"FieldValue": "2023-06-09"

},
{

"FieldName": "PLSEZ",

"FieldDesc": "End Date",

"FieldValue": "2026-06-08"

},
{

"FieldName": "PST1",

"FieldDesc": "POST1",

"FieldValue": ""

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

"FieldName": "Email",

"FieldDesc": "Requester E-Mail",

"FieldValue": "vamsi.nilla@email.com"

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

"FieldValue": 1

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


input_dictionary = dict()


for i in header.keys():
    input_dictionary[i] = header[i]
    print(i)

print(input_dictionary)



for j in body_list :

    k= j['FieldValue']

    if k == '':
        k= 0

    input_dictionary[j['FieldDesc']] = k

print(input_dictionary)

bulk_object = Bulk_Driver()
response = bulk_object.bulk_driver_method(header, body_list)
print("response after",response)




# Default_records_flag = 0
# PSPID_wbselement_flag = 0
# VBUKR_flag = 0
# Currentdate_flag = 0
# Finisheddate_flag = 0
#
# Current_date_value = ""
# Finisheddate_value = ""
#
# Number_of_Records = 0
# pat = pd.DataFrame([])
# paf = pd.DataFrame([])
#
# Process_area_flag = input("Please enter the process area")
#
# Default_records_flag = int(input("Please enter 1 for Default config_records else 0"))
#
# Current_date = input("Please enter required Currentdate(YYYY-MM-DD) else enter 0 if default")
#
# if Current_date == '0':
#     Current_date = datetime.date.today()
#
#     # add three years to the date
#     future_date = Current_date + datetime.timedelta(days=3 * 365)
#     Current_date = Current_date.strftime('%Y-%m-%d')
#     future_date = future_date.strftime('%Y-%m-%d')
# else:
#     Current_date = Current_date
#
# Finished_date = input("Please enter required Finisheddate(YYYY-MM-DD)  else enter 0 if default")
#
# if Finished_date == '0':
#     Current_date = datetime.date.today()
#
#     # add three years to the date
#     future_date = Current_date + datetime.timedelta(days=3 * 365)
#     Current_date = Current_date.strftime('%Y-%m-%d')
#     Finished_date = future_date.strftime('%Y-%m-%d')
# else:
#     Finished_date = Finished_date
#
# #Description_flag = input('Enter Description for RANDOM_TEXT else press enter key :')
#
# Number_of_Records = int(input("Please enter number of records to be generated"))
# complete_output=pd.DataFrame()
#
# # inputs
# VBUKR= int(input('Enter value of VBUKR or else press enter 0'))
# # PSPID = input('Enter value PSPID or else press enter 0')
# POST1 = input('Enter value of POST1 or else press enter 0')
# L2_levels = input('Enter value of L2 levels required or else press enter 0')
# # PLSEZ= input('Enter value of PLSEZ or else press enter key')
# # PRART= input('Enter value of PRART or else press enter key')
# # ZZCRMOPP = input('Enter value of ZZCRMOPP or else press enter key')
# MANDT = input('Enter Source system id or else press 0 for default JUPITER')
# ZZ_CLIENT = input('Enter value of ZZ_CLIENT or else press enter 0')
# EMAIl = input('Enter Requester E-Mail or else press 0 for default')
#
# # json ui
# input_data_dict = {
#     'Process_area_flag': Process_area_flag,
#     'Default_records_flag': Default_records_flag,
#     'Current_date': Current_date,
#     'Finished_date': Finished_date,
#     'Number_of_Records': Number_of_Records,
#     'random_state': 0,
#     'EMAIl': EMAIl,
#
#     #  'PSPID':PSPID,
#     'POST1':POST1,
#      'VBUKR': VBUKR,
#     #  'PLFAZ': PLFAZ,
#     #  'PLSEZ':PLSEZ,
#       'L2_levels':L2_levels,
#      'MANDT':MANDT,
#       'ZZ_CLIENT':ZZ_CLIENT
#
#     #   'input_filename_dict':'',
#     #    'historic_data':""
# }
#
#
#
# input_data_dict['random_state'] = random.randint(1, 50000)
#
# json_ui = json.dumps(input_data_dict)
