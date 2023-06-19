import pandas as pd

sdv_bulk = pd.read_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\BULK_CONFIG_FILE\Engagement_training_config_file.xlsx',sheet_name='SDV_BULK')

col_list = set(sdv_bulk['Template_field_name'].tolist())

gen_data = pd.read_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\concat_dataframe_final.xlsx')

gen_col_list = set(gen_data.columns.tolist())

print(col_list.symmetric_difference(gen_col_list))
