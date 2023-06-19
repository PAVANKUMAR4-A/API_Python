import pandas as pd
import numpy as np
import datetime
import json
import random
import string
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.sampling import Condition

class Default_data_gen():

    def Defaultdata_transformations(self,ENG_DV_df,parameter_value, json_ui, concat_dataframe,Historic_data_locations,Pickle_file_locations,Data_dependency,Pikcle_file_description):
        print("Defaultdata_transformations")
        print(ENG_DV_df)
        print(parameter_value)
        iterations = parameter_value.split('-')[1]
        iterations = int(iterations)
        result_dataframe = pd.DataFrame([])
        extracted_json = json.loads(json_ui)
        print('result_dataframe',result_dataframe)

        for index,row in Pickle_file_locations.iterrows():
            if row['Pikcle_file_description'].lower()==Pikcle_file_description.lower():
                saved_location = row['Saved_location']

        synthesizer = GaussianCopulaSynthesizer.load(
            filepath=saved_location
        )

        print(extracted_json['Number_of_Records'])
        #synthetic_temp_df = synthesizer.
        synthetic_data = synthesizer.sample(num_rows= iterations*int(extracted_json['Number_of_Records']))
        synthetic_data.to_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\sample_synthetic.xlsx')
        print(synthetic_data)
        return(synthetic_data)






