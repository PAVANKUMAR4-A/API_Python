from SDV_BULK_API_FILE import BULK_Pickle_file_config_file
from SDV_BULK_API_FILE.SDV_BULK_Autogen_Class_file import Autogen_variable_data_gen
from SDV_BULK_API_FILE.SDV_Master_data_gen_updated import Master_data_gen
from SDV_BULK_API_FILE.SDV_BULK_Default_data_gen import Default_data_gen
from SDV_BULK_API_FILE.SDV_BULK_Backend_data_gen import Backend_data_gen
from SDV_BULK_API_FILE.SDV_BULK_Text_data_gen import Text_data_gen
from SDV_BULK_API_FILE.SDV_BULK_Autogen_Class_Rule_dep_file import Autogen_variable_rule_dep_data_gen
from SDV_BULK_API_FILE.SDV_BULK_GET_Data_Display import Generated_data_display
import pandas as pd
import numpy as np
import datetime
import json
import random
import datetime as datetime
import time

class Bulk_Driver():

    def bulk_driver_method(self,header,body_list):

        print("entered bulk driver method")

        print(header,"header")
        print(body_list,"body")
        input_data_dictionary = dict()
        for i in header.keys():
            input_data_dictionary[i] = header[i]
            #print(i)

        for j in body_list:
            field_value = j['FieldValue']
            if field_value == '':
                field_value = 0
            input_data_dictionary[j['FieldDesc']] = field_value

        print(input_data_dictionary, "input_data_dictionary")

        #input_data_dictionary['random_state'] = random.randint(1, 50000)

        json_ui = json.dumps(input_data_dictionary)

        start = time.time()
        if int(input_data_dictionary['NumOfRecords']) != int(0):

            concat_dataframe = pd.DataFrame([])

            try:
                pickle_config = BULK_Pickle_file_config_file.Pickle_file_configuration()
                config_file = pickle_config.call_configuration_table(input_data_dictionary['ProcessAreaId'])

                print(config_file,"config file")

                for key, value in config_file.items():
                    if key.lower() == 'Historic_data_locations'.lower():
                        Historic_data_locations = value.loc[:, :]
                        print(Historic_data_locations,"historic data")
                    elif key.lower() == 'SDV_BULK'.lower():
                        sdv_metadata = value.loc[:, :]
                        # print(sdv_metadata)
                    elif key.lower() == 'Bulk_Data_dependency'.lower():
                        Data_dependency_df = value.loc[:, :]
                        # print(Data_dependency_df)
                    elif key.lower() == 'BULK_Pickle_file_locations'.lower():
                        Pickle_file_locations = value.loc[:, :]
                        # print(Pickle_file_locations)

                Display_data = sdv_metadata[sdv_metadata['Data_Display'] == 'Y']['Template_field_name']
                Display_data_columns = Display_data.tolist()
                print(Display_data_columns)


                sdv_metadata_Rule_indicator_list = sdv_metadata['Rule_indicator'].unique().tolist()
                #sdv_metadata_Rule_indicator_list.sort()
                print(sdv_metadata_Rule_indicator_list,"rule list")
                RL_dataframe = pd.DataFrame([])
                sdv_metadata_Rule_indicator_list = ['RL', 'MD', 'DV', 'BD', 'TXT', 'RLDP']  # ,'MD','DV','BD','TXT
                for rule in sdv_metadata_Rule_indicator_list:
                    print(rule,"rule text")
                    if rule.lower() == 'MD'.lower():
                        # print("Masterdata_values")
                        ENG_MD_df = sdv_metadata.loc[sdv_metadata['Rule_indicator'] == 'MD',]
                        function_name = ENG_MD_df['Function'].unique().tolist()[0]
                        parameter_value = ENG_MD_df['Parameter'].unique().tolist()[0]
                        Pikcle_file_description = ENG_MD_df['Pikcle_file_description'].unique().tolist()[0]
                        Data_dependency = Data_dependency_df
                        # print(function_name)
                        class_instance = Master_data_gen()
                        method_value = getattr(class_instance, function_name)
                        args = (ENG_MD_df, parameter_value, json_ui, concat_dataframe, Historic_data_locations,
                                Pickle_file_locations, Data_dependency, Pikcle_file_description)
                        result_dataframe = method_value(*args)
                        concat_dataframe = pd.concat([concat_dataframe, result_dataframe], axis=1)
                        # print(concat_dataframe)

                    elif rule.lower() == 'DV'.lower():
                        # print("Defaultdata_values")
                        ENG_DV_df = sdv_metadata.loc[sdv_metadata['Rule_indicator'] == 'DV',]
                        # print(ENG_DV_df[['Field_name','Function']])
                        # function_name = 'Defaultdata_transformations'#ENG_DV_df['Function'].unique().tolist()
                        function_name = ENG_DV_df['Function'].unique().tolist()[0]
                        # print('function_name',function_name)
                        parameter_value = ENG_DV_df['Parameter'].unique().tolist()[0]
                        # print(parameter_value)
                        Pikcle_file_description = ENG_DV_df['Pikcle_file_description'].unique().tolist()[0]
                        Data_dependency = Data_dependency_df
                        # print(function_name)
                        class_instance = Default_data_gen()
                        method_value = getattr(class_instance, function_name)
                        args = (ENG_DV_df, parameter_value, json_ui, concat_dataframe, Historic_data_locations,
                                Pickle_file_locations, Data_dependency, Pikcle_file_description)
                        result_dataframe = method_value(*args)
                        concat_dataframe = pd.concat([concat_dataframe, result_dataframe], axis=1)
                        # print(concat_dataframe)

                    elif rule.lower() == 'BD'.lower():
                        # print("Backend_deriveddata_values")
                        ENG_BD_df = sdv_metadata.loc[sdv_metadata['Rule_indicator'] == 'BD',]
                        # print(ENG_DV_df[['Field_name','Function']])
                        # function_name = 'Defaultdata_transformations'#ENG_DV_df['Function'].unique().tolist()
                        function_name = ENG_BD_df['Function'].unique().tolist()[0]
                        # print('function_name',function_name)
                        parameter_value = ENG_BD_df['Parameter'].unique().tolist()[0]
                        # print(parameter_value)
                        Pikcle_file_description = ENG_BD_df['Pikcle_file_description'].unique().tolist()[0]
                        Data_dependency = Data_dependency_df
                        # print(function_name)
                        class_instance = Backend_data_gen()
                        method_value = getattr(class_instance, function_name)
                        args = (ENG_BD_df, parameter_value, json_ui, concat_dataframe, Historic_data_locations,
                                Pickle_file_locations, Data_dependency, Pikcle_file_description)
                        result_dataframe = method_value(*args)
                        concat_dataframe = pd.concat([concat_dataframe, result_dataframe], axis=1)
                        # print(concat_dataframe)
                    elif rule.lower() == 'TXT'.lower():
                        # print("TXT_data_values")
                        ENG_TXT_df = sdv_metadata.loc[sdv_metadata['Rule_indicator'] == 'TXT',]
                        # print(ENG_DV_df[['Field_name','Function']])
                        # function_name = 'Defaultdata_transformations'#ENG_DV_df['Function'].unique().tolist()
                        function_name = ENG_TXT_df['Function'].unique().tolist()[0]
                        # print('function_name',function_name)
                        parameter_value = ENG_TXT_df['Parameter'].unique().tolist()[0]
                        # print("parameter_valuebefore",parameter_value)
                        Pikcle_file_description = ENG_TXT_df['Pikcle_file_description'].unique().tolist()[0]
                        Data_dependency = Data_dependency_df
                        # print(function_name)
                        class_instance = Text_data_gen()
                        method_value = getattr(class_instance, function_name)
                        args = (ENG_TXT_df, parameter_value, json_ui, concat_dataframe, Historic_data_locations,
                                Pickle_file_locations, Data_dependency, Pikcle_file_description)
                        result_dataframe = method_value(*args)
                        concat_dataframe = pd.concat([concat_dataframe, result_dataframe], axis=1)
                        # print(concat_dataframe)




                    elif rule.lower() == 'RL'.lower():
                        ENG_RL_df = sdv_metadata.loc[sdv_metadata['Rule_indicator'] == 'RL',]
                        # print(ENG_RL_df)

                        for index, row in ENG_RL_df.iterrows():
                            class_instance = Autogen_variable_data_gen()
                            function_name = row['Function']
                            parameter_value = row['Parameter']
                            Data_dependency = row['Data_dependency']

                            column_name = row['Template_field_name']
                            # print("column_name reached",column_name)
                            # print(function_name)
                            method_value = getattr(class_instance, function_name)
                            args = (column_name, parameter_value, Data_dependency, json_ui, concat_dataframe)
                            result_dataframe = method_value(*args)
                            concat_dataframe = pd.concat([concat_dataframe, result_dataframe], axis=1)

                            # print(concat_dataframe)


                    elif rule.lower() == 'RLDP'.lower():
                        ENG_RLDP_df = sdv_metadata.loc[sdv_metadata['Rule_indicator'] == 'RLDP',]
                        # print(ENG_RL_df)
                        function_name = ENG_RLDP_df['Function'].unique().tolist()[0]
                        parameter_value = ENG_RLDP_df['Parameter'].unique().tolist()[0]
                        # Pikcle_file_description = ENG_MD_df['Pikcle_file_description'].unique().tolist()[0]
                        Data_dependency = Data_dependency_df
                        # print(function_name)
                        class_instance = Autogen_variable_rule_dep_data_gen()
                        method_value = getattr(class_instance, function_name)
                        args = (
                            ENG_RLDP_df, parameter_value, json_ui, concat_dataframe, Historic_data_locations,
                            Data_dependency_df)
                        result_dataframe = method_value(*args)
                        concat_dataframe = result_dataframe
                        #print(result_dataframe)


                concat_dataframe.reset_index(drop=True, inplace=True)


                end = time.time()
                print("The time of execution of above program is :",
                      (end - start) * 10 ** 3, "ms")
                concat_dataframe.to_excel(
                    r'D:\Users\pavankumar4\PycharmProjects\Latest_Python_Vamsi_Code\sample_synthetic\concat_dataframe_final.xlsx')
                #print("bulk_updated_concat_dict",concat_dataframe)
                #print("bulk_updated_input_dict", input_data_dictionary)
                #return [concat_dataframe,input_data_dictionary]

            except Exception as e:
                print(e)
            print("returning statement bulk")
        # print("bulk_updated_concat_dict", concat_dataframe)
        # print("bulk_updated_input_dict", input_data_dictionary)
        return [concat_dataframe,input_data_dictionary]
