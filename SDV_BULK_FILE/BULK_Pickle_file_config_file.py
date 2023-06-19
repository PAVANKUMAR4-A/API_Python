import pandas as pd
import numpy as np


class Pickle_file_configuration():

    def __init__(self):
        self.configuration_file = r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\BULK_CONFIG_FILE\Engagement_training_config_file.xlsx'

    def call_configuration_table(self, Process_area):

        try:

            Table_dictionary = dict()
            Process_area_code = ""
            config_file = pd.read_excel(self.configuration_file, sheet_name='Config_table_flow')

            #print(config_file)

            Table_names = config_file['Table_names'].tolist()
            for table in Table_names:
                # reading each sheet and assigning sheet names as keys and complete sheet info as values
                Table_dictionary[table] = pd.read_excel(self.configuration_file, sheet_name=str(table))

            #print(Table_dictionary)
            # for table in Table_names:
            #     if table.lower() == 'Process_Areas'.lower():
            #
            #         # fetching columns in Process_Areas
            #         for col in Table_dictionary[table].columns:
            #
            #             if Process_area in Table_dictionary[table][col].values:
            #                 row_index = Table_dictionary[table].index[Table_dictionary[table][col] == Process_area].tolist()[0]
            #
            #                 # fetching 'Process_Area' records
            #                 Process_area_code = Table_dictionary[table].loc[row_index, 'Process_Area']

            for table2 in Table_names:
                # creating dictionary with sheetnames as keys and all matched sheet data as values
                #print(table2)
                Table_dictionary[table2] = Table_dictionary[table2][Table_dictionary[table2]['Process_Area'] == Process_area]
            #print(Table_dictionary)
            return Table_dictionary


        except Exception as e:
            print(e)
            return (e)

