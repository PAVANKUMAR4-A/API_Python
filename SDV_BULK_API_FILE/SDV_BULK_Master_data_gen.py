import pandas as pd
import numpy as np
import datetime
import json
import random
import string
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.sampling import Condition

class Master_data_gen():



    def Masterdata_transformations(self,ENG_MD_df,parameter_value, json_ui, concat_dataframe,Historic_data_locations,Pickle_file_locations,Data_dependency,Pikcle_file_description):
        print("Masterdata_transformations")
        #print(ENG_MD_df)
        #print(parameter_value)
        iterations = parameter_value.split('-')[1]
        iterations = int(iterations)
        result_dataframe = pd.DataFrame([])
        extracted_json = json.loads(json_ui)
        #print('result_dataframe',result_dataframe)

        for index,row in Pickle_file_locations.iterrows():
            if row['Pikcle_file_description'].lower()==Pikcle_file_description.lower():
                saved_location = row['Saved_location']


        synthesizer = GaussianCopulaSynthesizer.load(
            filepath=saved_location
        )

        print(extracted_json['NumOfRecords'])
        print(extracted_json['Entity'])


        if str(extracted_json['Entity']) == str(0):
            synthetic_data_temp = synthesizer.sample(num_rows=int(extracted_json['NumOfRecords']))
            synthetic_data = synthetic_data_temp.loc[sorted([*synthetic_data_temp.index] * iterations)].reset_index(
                drop=True)
            synthetic_data.to_excel(
                r'D:\Users\pavankumar4\PycharmProjects\Latest_Python_Vamsi_Code\sample_synthetic\sample_synthetic_master.xlsx')
            print(synthetic_data)

        else :

            VBUKR_condition = Condition(
                num_rows=int(extracted_json['NumOfRecords']),
                column_values={'Entity': extracted_json['Entity']}
            )
            synthetic_data_temp = synthesizer.sample_from_conditions(
                conditions=[VBUKR_condition],
                output_file_path=None
            )
            synthetic_data = synthetic_data_temp.loc[sorted([*synthetic_data_temp.index] * iterations)].reset_index(
                drop=True)
            synthetic_data.to_excel(
                r'D:\Users\pavankumar4\PycharmProjects\Latest_Python_Vamsi_Code\sample_synthetic\sample_synthetic_master.xlsx')
            print(synthetic_data)
            #return (synthetic_data)


        # df = pd.melt(synthetic_data, id_vars='PRJ-PRPS-WBSELEMENT-S', value_vars=['Y3', 'Z3', 'Z4', 'Z6', 'Z1', 'Z2', 'Z8', 'Z9'],
        #              var_name='PRJ-IHPA-PARVW-S', value_name='PRJ-IHPA-PARNR-S')
        # g = df.merge(synthetic_data, how='inner', on='PRJ-PRPS-WBSELEMENT-S')
        # g.to_excel(
        #     r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\sample_synthetic_master.xlsx')

        #return(g)

        return (synthetic_data)












