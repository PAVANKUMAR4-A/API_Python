import pandas as pd
import numpy as np

master = pd.read_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\BULK_Masterdata_location\BULK_updated.xlsx')

print(master.columns)








# collist = pd.read_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\BULK_Masterdata_location\BULK_masterdata.xlsx',sheet_name='columns')
#
# k= collist['column_list'].tolist()
# k= set(k)
# m= set(master.columns.tolist())
# print(len(k.intersection(m)))
# # print(k)
# # print(master.columns)
# df = master[k]
# df.to_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\BULK_Masterdata_location\Master_df.xlsx')