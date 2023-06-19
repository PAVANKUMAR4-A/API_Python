import pandas as pd
import numpy as np
import datetime
import json
import random
import string


class Autogen_variable_data_gen():




    def STATIC_DATA(self,column_name, parameter_value, Data_dependency, json_ui, concat_dataframe):
        print("Static_data_function")
        print(parameter_value)
        extracted_json = json.loads(json_ui)


        result_df_temp = pd.DataFrame([])
        parameter_split  = parameter_value.split('@')
        iterations = parameter_split[1].split('-')[1]
        static_value  = parameter_split[0].split('=')[1]
        static_list = static_value.split(',')
        result_df_temp[column_name] = static_list* int(extracted_json['Number_of_Records'])
        result_df = result_df_temp.loc[sorted([*result_df_temp.index] * int(iterations))].reset_index(drop=True)
        return (result_df)




    def WBS_ID(self,column_name, parameter_value, Data_dependency, json_ui, concat_dataframe):

        if Data_dependency.lower()=='N'.lower():
            print("function_wbs_id")
            concat_dataframe = concat_dataframe
            result_dataframe = pd.DataFrame([])
            extracted_json = json.loads(json_ui)
            #print(extracted_json['Number_of_Records'])
            parameter_value_list = parameter_value.split(',')
            #print(parameter_value_list)

            try:
                string_list = []
                for i in range(extracted_json['Number_of_Records']):
                    string_value = ""

                    for param in parameter_value_list:
                        column_list = []
                        if 'ALPHA'.lower() in param.lower():
                            param_split = param.split('-')
                            letters = random.sample(string.ascii_uppercase, int(param_split[1]))
                            alpha_prefix = "".join(letters)
                            string_value = string_value + alpha_prefix
                            #print(string_value)
                        elif 'SYN'.lower() in param.lower():
                            param_split = param.split('-')
                            syn_prefix = param_split[1]
                            string_value = string_value + syn_prefix
                            #print(string_value)
                        elif 'RANDOM_NUM'.lower() in param.lower():
                            param_split = param.split('-')
                            random_prefix = "".join(random.sample(string.digits, int(param_split[1])))
                            string_value = string_value + random_prefix
                            #print(string_value)

                        elif 'ITER'.lower() in param.lower():
                            param_split = param.split('-')
                            iterations  = int(param_split[1])
                            column_list = [string_value]*iterations
                            string_list.extend(column_list)

                        else:
                            string_value = "parameters wrong"
                result_dataframe[column_name] = string_list
                return(result_dataframe)

            except Exception as e:
                print(e)
                return (e)

        else:
            print("function_wbs_id_else")
            concat_dataframe = concat_dataframe
            result_dataframe = pd.DataFrame([])
            extracted_json = json.loads(json_ui)
            print(extracted_json['Number_of_Records'])
            parameter_value_list = parameter_value.split(',')
            print(parameter_value_list)


    def DATE_COLUMN(self,column_name, parameter_value, Data_dependency, json_ui, concat_dataframe):
        print("date_column")

        value_list = []


        result_df = pd.DataFrame([])
        extracted_json = json.loads(json_ui)
        parameter_value_split = parameter_value.split(',')
        iterations_split = parameter_value_split[2].split('-')
        iterations = iterations_split[1]

        if parameter_value_split[0].lower() == 'start'.lower():
            value = extracted_json['Current_date']
        else:
            value = extracted_json['Finished_date']

        value_list.append(value)
        value_list_iter = value_list*int(iterations)*int(extracted_json['Number_of_Records'])
        result_df[column_name] = value_list_iter
        return(result_df)










