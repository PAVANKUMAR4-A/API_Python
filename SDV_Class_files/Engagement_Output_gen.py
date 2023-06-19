import pandas as pd
import numpy as np

class Output_data_gen():

    def Output_data_transformations(self,concat_dataframe,Historic_data_locations,sdv_metadata):

        print("output_data_transformations")
        print(concat_dataframe['PRJ-PRPS-WBSELEMENT-S'].unique().tolist())
        subprocess_dict = dict()
        subprocess_list = sdv_metadata['Sub_process_area'].unique().tolist()
        sdv_dataframe_temp = sdv_metadata.copy()
        table_list = sdv_metadata['Table_name'].unique().tolist()
        # Output_file_list = sdv_metadata['Output_file_list'].unique().tolist()

        sdv_dataframe_temp['collist'] = sdv_metadata['Sub_process_area'] + '-' + sdv_metadata['Table_name'] + '-' + \
                                           sdv_metadata['Field_name'] + '-' + sdv_metadata['Output_file']
        table_dict = dict()

        out_s = sdv_dataframe_temp[sdv_dataframe_temp['Output_file'] == 'S']
        out_c = sdv_dataframe_temp[sdv_dataframe_temp['Output_file'] == 'C']

        output_dic = dict()

        for tables in table_list:

            k = out_s[out_s['Table_name'] == tables]['collist'].tolist()
            if len(k) != 0:
                output_dic[tables] = k

        for subproc in subprocess_list:

            f = out_c[out_c['Sub_process_area'] == subproc]['collist'].tolist()
            if len(f) != 0:
                output_dic[subproc] = f

        concat_df = concat_dataframe

        for key in output_dic:
            print(key)
            res_df = pd.DataFrame([])
            print(output_dic[key])
            k = output_dic[key]
            res_df = concat_df[output_dic[key]]
            final_col = []
            init_col = res_df.columns.tolist()
            for i in init_col:
                t = i.split('-')[2]
                final_col.append(t)
            print("saving_file ",key)
            res_df.set_axis(final_col, axis='columns', inplace=True)
            # df.to_csv(r'c:\data\pandas.txt', header=None, index=None, sep=' ', mode='a')
            res_df.to_excel('C:\\Users\\vamsikkrishna\\PycharmProjects\\pythonProject1\\Output_Files_Directory\\' + key + '.xlsx')
            res_df.to_csv(
                'C:\\Users\\vamsikkrishna\\PycharmProjects\\pythonProject1\\Output_Files_Directory\\' + key + '.txt',
                sep=' ')
            return ("process completed")




