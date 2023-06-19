# from sdv.single_table import GaussianCopulaSynthesizer
# from sdv.sampling import Condition
#
# saved_location = r'C:\Users\vamsikkrishna\PycharmProjects\sdg_sdv\Pickle_file_locations\Engagement_Default_values_pickle_file\Engagement_Default_values_pickle_file.pkl'
#
# saved_location=r'C:\Users\vamsikkrishna\PycharmProjects\sdg_sdv\Pickle_file_locations\Engagement_Default_values_pickle_file\Engagement_Default_values_pickle_file.pkl'
# synthesizer = GaussianCopulaSynthesizer.load(
#             filepath=saved_location
#         )
#
# print(synthesizer.get_metadata())
# synthetic_data = synthesizer.sample(num_rows=100)
# print(synthetic_data)

import pandas as pd

temp_df = pd.DataFrame([])

sdv_metadata = pd.read_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\Engagement_training_config_file\Engagement_training_config_file.xlsx',sheet_name='sdv_metadata')
subprocess_dict = dict()
subprocess_list = sdv_metadata['Sub_process_area'].unique().tolist()
concat_dataframe_temp = sdv_metadata.copy()
table_list = sdv_metadata['Table_name'].unique().tolist()
#Output_file_list = sdv_metadata['Output_file_list'].unique().tolist()

concat_dataframe_temp['collist'] = sdv_metadata['Sub_process_area'] + '-' + sdv_metadata['Table_name'] + '-' + \
                                   sdv_metadata['Field_name'] + '-' + sdv_metadata['Output_file']
table_dict = dict()



out_s = concat_dataframe_temp[concat_dataframe_temp['Output_file']=='S']
out_c = concat_dataframe_temp[concat_dataframe_temp['Output_file']=='C']

output_dic = dict()

for tables in table_list:

    k= out_s[out_s['Table_name']==tables]['collist'].tolist()
    if len(k)!= 0:
        output_dic[tables] = k


for subproc in subprocess_list:

    f = out_c[out_c['Sub_process_area']==subproc]['collist'].tolist()
    if len(f)!=0:
        output_dic[subproc] = f

print(output_dic)


concat_df = pd.read_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\concat_dataframe_final.xlsx')

output_file_dict = ()

for key in output_dic:
    print(key)
    res_df = pd.DataFrame([])
    print(output_dic[key])
    k= output_dic[key]
    res_df = concat_df[output_dic[key]]
    final_col = []
    init_col = res_df.columns.tolist()
    for i in init_col:
        t = i.split('-')[2]
        final_col.append(t)

    init_col = res_df.columns.tolist()
    res_df.set_axis(final_col, axis='columns', inplace=True)

    if key == 'PROJ':
        res_df.drop_duplicates(subset=['POSID'],inplace=True)
    elif key == 'PRPS':
        res_df.drop_duplicates(subset=['WBSELEMENT'],inplace=True)
    elif key == 'ZTCTC_PROJ_AU':
        res_df.drop_duplicates(subset=['PSPID'], inplace=True)
    elif key == 'ZTCTC_PROJ_GLB':
        res_df.drop_duplicates(subset=['PSPID'], inplace=True)
    elif key == 'FIN':
        res_df.drop_duplicates(subset=['MP_ITEM_OKEY'],inplace=True)




    print("saving to ",'C:\\Users\\vamsikkrishna\\PycharmProjects\\pythonProject1\\Output_Files_Directory\\'+key+'.txt')
    #df.to_csv(r'c:\data\pandas.txt', header=None, index=None, sep=' ', mode='a')
    res_df.to_csv('C:\\Users\\vamsikkrishna\\PycharmProjects\\pythonProject1\\Output_Files_Directory\\'+key+'.txt',sep=' ')
    res_df.to_excel('C:\\Users\\vamsikkrishna\\PycharmProjects\\pythonProject1\\Output_Files_Directory\\' + key + '.xlsx')

