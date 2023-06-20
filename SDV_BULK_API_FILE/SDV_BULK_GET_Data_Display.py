import pandas as pd
import  numpy as np
from SDV_BULK_API_FILE import BULK_Pickle_file_config_file
import openpyxl
#pickle_config = BULK_Pickle_file_config_file.Pickle_file_configuration()
#config_file = pickle_config.call_configuration_table(input_data_dictionary['ProcessAreaId'])


class Generated_data_display():

    # def __init__(self):
    #     self.pickle_config = BULK_Pickle_file_config_file.Pickle_file_configuration()

    def Screen_Data_display(self,concat_dataframe,input_data_dictionary):
        print("vamsi_krishna")
        print("concat_dataframe",concat_dataframe)


        pickle_config = BULK_Pickle_file_config_file.Pickle_file_configuration()
        config_file = pickle_config.call_configuration_table(input_data_dictionary['ProcessAreaId'])

        for key, value in config_file.items():
            if key.lower() == 'SDV_BULK'.lower():
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
        #print(Display_data_columns)

        filtered_display_data = concat_dataframe[Display_data_columns]

        print('Filtered Data', filtered_display_data)
        return(filtered_display_data)