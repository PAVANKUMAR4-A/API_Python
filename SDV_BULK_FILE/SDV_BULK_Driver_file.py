
#from SDV_Class_files import Pickle_file_config_file
from SDV_BULK_FILE import BULK_Pickle_file_config_file
#from SDV_Class_files.Autogen_Class_file import Autogen_variable_data_gen
from SDV_BULK_FILE.SDV_BULK_Autogen_Class_file import Autogen_variable_data_gen
#from SDV_Class_files.Engagement_Master_data_gen import Master_data_gen
#from SDV_BULK_FILE.SDV_BULK_Master_data_gen import Master_data_gen
from SDV_BULK_FILE.SDV_Master_data_gen_updated import Master_data_gen
#from SDV_Class_files.Engagement_Default_data_gen import Default_data_gen
from SDV_BULK_FILE.SDV_BULK_Default_data_gen import Default_data_gen
#from SDV_Class_files.Engagement_Backend_data_gen import Backend_data_gen
from SDV_BULK_FILE.SDV_BULK_Backend_data_gen import Backend_data_gen
#from SDV_Class_files.Engagement_Text_data_gen import Text_data_gen
from SDV_BULK_FILE.SDV_BULK_Text_data_gen import Text_data_gen
#from SDV_Class_files.Autogen_Class_Rule_dep_file import Autogen_variable_rule_dep_data_gen
from SDV_BULK_FILE.SDV_BULK_Autogen_Class_Rule_dep_file import Autogen_variable_rule_dep_data_gen
#from SDV_Class_files.Engagement_Output_gen import Output_data_gen
#from SDV_Class_files.h import Master_data_gen
import pandas as pd
import numpy as np
import datetime
import json
import random
import datetime as datetime
import time

Default_records_flag = 0
PSPID_wbselement_flag = 0
VBUKR_flag = 0
Currentdate_flag = 0
Finisheddate_flag = 0

Current_date_value = ""
Finisheddate_value = ""

Number_of_Records = 0
pat = pd.DataFrame([])
paf = pd.DataFrame([])

Process_area_flag = input("Please enter the process area")

Default_records_flag = int(input("Please enter 1 for Default config_records else 0"))

Current_date = input("Please enter required Currentdate(YYYY-MM-DD) else enter 0 if default")

if Current_date == '0':
    Current_date = datetime.date.today()

    # add three years to the date
    future_date = Current_date + datetime.timedelta(days=3 * 365)
    Current_date = Current_date.strftime('%Y-%m-%d')
    future_date = future_date.strftime('%Y-%m-%d')
else:
    Current_date = Current_date

Finished_date = input("Please enter required Finisheddate(YYYY-MM-DD)  else enter 0 if default")

if Finished_date == '0':
    Current_date = datetime.date.today()

    # add three years to the date
    future_date = Current_date + datetime.timedelta(days=3 * 365)
    Current_date = Current_date.strftime('%Y-%m-%d')
    Finished_date = future_date.strftime('%Y-%m-%d')
else:
    Finished_date = Finished_date

#Description_flag = input('Enter Description for RANDOM_TEXT else press enter key :')

Number_of_Records = int(input("Please enter number of records to be generated"))
complete_output=pd.DataFrame()

# inputs
VBUKR= int(input('Enter value of VBUKR or else press enter 0'))
# PSPID = input('Enter value PSPID or else press enter 0')
POST1 = input('Enter value of POST1 or else press enter 0')
L2_levels = input('Enter value of L2 levels required or else press enter 0')
# PLSEZ= input('Enter value of PLSEZ or else press enter key')
# PRART= input('Enter value of PRART or else press enter key')
# ZZCRMOPP = input('Enter value of ZZCRMOPP or else press enter key')
MANDT = input('Enter Source system id or else press 0 for default JUPITER')
ZZ_CLIENT = input('Enter value of ZZ_CLIENT or else press enter 0')
EMAIl = input('Enter Requester E-Mail or else press 0 for default')

# json ui
input_data_dict = {
    'Process_area_flag': Process_area_flag,
    'Default_records_flag': Default_records_flag,
    'Current_date': Current_date,
    'Finished_date': Finished_date,
    'Number_of_Records': Number_of_Records,
    'random_state': 0,
    'EMAIl': EMAIl,

    #  'PSPID':PSPID,
    'POST1':POST1,
     'VBUKR': VBUKR,
    #  'PLFAZ': PLFAZ,
    #  'PLSEZ':PLSEZ,
      'L2_levels':L2_levels,
     'MANDT':MANDT,
      'ZZ_CLIENT':ZZ_CLIENT

    #   'input_filename_dict':'',
    #    'historic_data':""
}

input_data_dict['random_state'] = random.randint(1, 50000)

json_ui = json.dumps(input_data_dict)

start = time.time()
if Number_of_Records != 0:

    concat_dataframe = pd.DataFrame([])

    try:
        pickle_config = BULK_Pickle_file_config_file.Pickle_file_configuration()
        config_file = pickle_config.call_configuration_table(Process_area_flag)

        for key, value in config_file.items():
            if key.lower() == 'Historic_data_locations'.lower():
                Historic_data_locations = value.loc[:, :]
                #print(Historic_data_locations)
            elif key.lower() == 'SDV_BULK'.lower():
                sdv_metadata = value.loc[:, :]
                #print(sdv_metadata)
            elif key.lower() == 'Bulk_Data_dependency'.lower():
                Data_dependency_df = value.loc[:,:]
                #print(Data_dependency_df)
            elif key.lower() == 'BULK_Pickle_file_locations'.lower():
                Pickle_file_locations = value.loc[:,:]
                #print(Pickle_file_locations)



        sdv_metadata_Rule_indicator_list = sdv_metadata['Rule_indicator'].unique().tolist()
        sdv_metadata_Rule_indicator_list.sort()
        print(sdv_metadata_Rule_indicator_list)
        RL_dataframe = pd.DataFrame([])
        sdv_metadata_Rule_indicator_list = ['RL','MD','DV','BD','TXT','RLDP']#,'MD','DV','BD','TXT
        for rule in sdv_metadata_Rule_indicator_list:

#C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\Pickle_file_locations\Engagement_Backend_Derived_Pickle_file

            if rule.lower() == 'MD'.lower():
                #print("Masterdata_values")
                ENG_MD_df = sdv_metadata.loc[sdv_metadata['Rule_indicator'] == 'MD',]
                function_name = ENG_MD_df['Function'].unique().tolist()[0]
                parameter_value = ENG_MD_df['Parameter'].unique().tolist()[0]
                Pikcle_file_description =ENG_MD_df['Pikcle_file_description'].unique().tolist()[0]
                Data_dependency = Data_dependency_df
                #print(function_name)
                class_instance = Master_data_gen()
                method_value = getattr(class_instance, function_name)
                args = (ENG_MD_df,parameter_value, json_ui, concat_dataframe,Historic_data_locations,Pickle_file_locations,Data_dependency,Pikcle_file_description)
                result_dataframe = method_value(*args)
                concat_dataframe = pd.concat([concat_dataframe, result_dataframe], axis=1)
                #print(concat_dataframe)

            elif rule.lower() == 'DV'.lower():
                #print("Defaultdata_values")
                ENG_DV_df = sdv_metadata.loc[sdv_metadata['Rule_indicator'] == 'DV',]
                #print(ENG_DV_df[['Field_name','Function']])
                #function_name = 'Defaultdata_transformations'#ENG_DV_df['Function'].unique().tolist()
                function_name = ENG_DV_df['Function'].unique().tolist()[0]
                #print('function_name',function_name)
                parameter_value = ENG_DV_df['Parameter'].unique().tolist()[0]
                #print(parameter_value)
                Pikcle_file_description =ENG_DV_df['Pikcle_file_description'].unique().tolist()[0]
                Data_dependency = Data_dependency_df
                #print(function_name)
                class_instance = Default_data_gen()
                method_value = getattr(class_instance, function_name)
                args = (ENG_DV_df,parameter_value, json_ui, concat_dataframe,Historic_data_locations,Pickle_file_locations,Data_dependency,Pikcle_file_description)
                result_dataframe = method_value(*args)
                concat_dataframe = pd.concat([concat_dataframe, result_dataframe], axis=1)
                #print(concat_dataframe)

            elif rule.lower() == 'BD'.lower():
                #print("Backend_deriveddata_values")
                ENG_BD_df = sdv_metadata.loc[sdv_metadata['Rule_indicator'] == 'BD',]
                #print(ENG_DV_df[['Field_name','Function']])
                #function_name = 'Defaultdata_transformations'#ENG_DV_df['Function'].unique().tolist()
                function_name = ENG_BD_df['Function'].unique().tolist()[0]
                #print('function_name',function_name)
                parameter_value = ENG_BD_df['Parameter'].unique().tolist()[0]
                #print(parameter_value)
                Pikcle_file_description =ENG_BD_df['Pikcle_file_description'].unique().tolist()[0]
                Data_dependency = Data_dependency_df
                #print(function_name)
                class_instance = Backend_data_gen()
                method_value = getattr(class_instance, function_name)
                args = (ENG_BD_df,parameter_value, json_ui, concat_dataframe,Historic_data_locations,Pickle_file_locations,Data_dependency,Pikcle_file_description)
                result_dataframe = method_value(*args)
                concat_dataframe = pd.concat([concat_dataframe, result_dataframe], axis=1)
                #print(concat_dataframe)
            elif rule.lower() == 'TXT'.lower():
                #print("TXT_data_values")
                ENG_TXT_df = sdv_metadata.loc[sdv_metadata['Rule_indicator'] == 'TXT',]
                #print(ENG_DV_df[['Field_name','Function']])
                #function_name = 'Defaultdata_transformations'#ENG_DV_df['Function'].unique().tolist()
                function_name = ENG_TXT_df['Function'].unique().tolist()[0]
                #print('function_name',function_name)
                parameter_value = ENG_TXT_df['Parameter'].unique().tolist()[0]
                #print("parameter_valuebefore",parameter_value)
                Pikcle_file_description =ENG_TXT_df['Pikcle_file_description'].unique().tolist()[0]
                Data_dependency = Data_dependency_df
                #print(function_name)
                class_instance = Text_data_gen()
                method_value = getattr(class_instance, function_name)
                args = (ENG_TXT_df,parameter_value, json_ui, concat_dataframe,Historic_data_locations,Pickle_file_locations,Data_dependency,Pikcle_file_description)
                result_dataframe = method_value(*args)
                concat_dataframe = pd.concat([concat_dataframe, result_dataframe], axis=1)
                #print(concat_dataframe)




            elif rule.lower() == 'RL'.lower():
                ENG_RL_df = sdv_metadata.loc[sdv_metadata['Rule_indicator']=='RL',]
                #print(ENG_RL_df)


                for index,row in ENG_RL_df.iterrows():
                    class_instance = Autogen_variable_data_gen()
                    function_name = row['Function']
                    parameter_value = row['Parameter']
                    #print(parameter_value)
                    #Sub_process_area = row['Sub_process_area']
                    #print(Sub_process_area)
                    #Table_name = row['Table_name']
                    #Field_name = row['Field_name']
                    #Output_file = row['Output_file']
                    Data_dependency = row['Data_dependency']
                    #print(Data_dependency)
                    #column_name = Sub_process_area+'-'+Table_name+'-'+Field_name+'-'+Output_file
                    column_name = row['Template_field_name']
                    #print("column_name reached",column_name)
                    #print(function_name)
                    method_value = getattr(class_instance, function_name)
                    args = (column_name, parameter_value, Data_dependency, json_ui, concat_dataframe)
                    result_dataframe = method_value(*args)
                    concat_dataframe = pd.concat([concat_dataframe, result_dataframe], axis=1)

                    #print(concat_dataframe)


            elif rule.lower() == 'RLDP'.lower():
                ENG_RLDP_df = sdv_metadata.loc[sdv_metadata['Rule_indicator']=='RLDP',]
                #print(ENG_RL_df)
                function_name = ENG_RLDP_df['Function'].unique().tolist()[0]
                parameter_value = ENG_RLDP_df['Parameter'].unique().tolist()[0]
                #Pikcle_file_description = ENG_MD_df['Pikcle_file_description'].unique().tolist()[0]
                Data_dependency = Data_dependency_df
                #print(function_name)
                class_instance = Autogen_variable_rule_dep_data_gen()
                method_value = getattr(class_instance, function_name)
                args = (
                ENG_RLDP_df, parameter_value, json_ui, concat_dataframe, Historic_data_locations,
                Data_dependency_df)
                result_dataframe = method_value(*args)
                concat_dataframe = result_dataframe
                print(result_dataframe)

        concat_dataframe.reset_index(drop=True, inplace=True)
        end = time.time()
        print("The time of execution of above program is :",
              (end - start) * 10 ** 3, "ms")
        concat_dataframe.to_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\concat_dataframe_final.xlsx')

        # output_class_instance = Output_data_gen()
        # function_name = 'Output_data_transformations'
        # method_value = getattr(output_class_instance, function_name)
        # args = (result_dataframe,Historic_data_locations,sdv_metadata)#concat_dataframe,Historic_data_locations,sdv_metadata
        # result_dataframe = method_value(*args)
        # print(result_dataframe)



    except Exception as e:
        print(e)















