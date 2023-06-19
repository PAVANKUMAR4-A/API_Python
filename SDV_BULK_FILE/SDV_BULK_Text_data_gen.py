import pandas as pd
import numpy as np
import datetime
import json
import random
import string
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.sampling import Condition

class Text_data_gen():

    def Textdata_transformations(self,ENG_MD_df,parameter_value, json_ui, concat_dataframe,Historic_data_locations,Pickle_file_locations,Data_dependency,Pikcle_file_description):
        print("textdata_transformations")
        #print(ENG_MD_df)
        print(parameter_value)
        iterations = parameter_value.split('-')[1]
        print("textdata iterations =",iterations,parameter_value)
        iterations = int(iterations)
        result_dataframe = pd.DataFrame([])
        extracted_json = json.loads(json_ui)
        #print('result_dataframe',result_dataframe)
        number_of_l2_required = int(extracted_json['L2_levels'])


        for index,row in Pickle_file_locations.iterrows():
            if row['Pikcle_file_description'].lower() == Pikcle_file_description.lower():
                saved_location = row['Saved_location']


        synthesizer = GaussianCopulaSynthesizer.load(
            filepath=saved_location
        )

        print(extracted_json['Number_of_Records'])
        synthetic_data_temp = synthesizer.sample(num_rows=int(extracted_json['Number_of_Records']))

        if str(extracted_json['POST1']) != str(0):
            print(extracted_json['POST1'])
            text_list = []
            for i in range(int(extracted_json['Number_of_Records'])):
                txt_value = str(extracted_json['POST1'])+'_'+str(i)
                text_list.append(txt_value)
            txt_columns_list = synthetic_data_temp.columns.tolist()
            for col in txt_columns_list:
                synthetic_data_temp[col] = text_list



        if number_of_l2_required == int(1):

            synthetic_data = synthetic_data_temp.loc[sorted([*synthetic_data_temp.index] * iterations)].reset_index(drop=True)

        else:

            synthetic_data = synthetic_data_temp.loc[sorted([*synthetic_data_temp.index] * int(number_of_l2_required))].reset_index(
                drop=True)





        synthetic_data.to_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\sample_synthetic_text.xlsx')
        print(synthetic_data)
        return(synthetic_data)






