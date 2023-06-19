import pandas as pd
import numpy as np
from faker import Faker
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata
from sdv.constraints import FixedCombinations
from SDV_Class_files import Pickle_file_config_file
pickle_config = Pickle_file_config_file.Pickle_file_configuration()
Process_area_code = 'ENG'
config_file = pickle_config.call_configuration_table(Process_area_code)
#print(config_file)


Historic_data_locations = config_file['Historic_data_locations']
Join_conditions = config_file['Join_conditions']
sdv_metadata = config_file['sdv_metadata']
Constraints = config_file['Constraints']
Pickle_file_locations = config_file['Pickle_file_locations']
TXT_words = config_file['TXT_words']

Save_pickle_dict =dict()

Historic_data = dict()


for index,row in Pickle_file_locations.iterrows():
    Save_pickle_dict[row['Pikcle_file_description']]= row['Saved_location']

print(Save_pickle_dict)



for index,row in Historic_data_locations.iterrows():
    filter_columns = row['Column_values'].split(',')

    Historic_data[row['Sub_process_area']] = pd.read_excel(row['Historic_data_locations'])
    print(filter_columns)
    print(Historic_data[row['Sub_process_area']].columns)
    Historic_data[row['Sub_process_area']] = Historic_data[row['Sub_process_area']][filter_columns]

Historic_data['PRJ']['CLIENT'] = Historic_data['PRJ']['ZZ_CLIENT']

sdv_metadata_md = sdv_metadata[sdv_metadata['Rule_indicator']=='MD']

sdv_metadata_md['column_name'] = sdv_metadata_md['Sub_process_area']+'-'+sdv_metadata_md['Table_name']+'-'+sdv_metadata_md['Field_name']+'-'+sdv_metadata_md['Output_file']

Masterdata_columns = sdv_metadata_md['column_name'].tolist()
print(Masterdata_columns)

sdv_metadata_table_names = sdv_metadata['Table_name'].unique().tolist()
# print(sdv_metadata_table_names)

# dictionary_for_output_table = dict()

PRJ_id_columns = ['POSID','PSPNR','OBJNR']
FIN_id_columns = ['PSPNR','PSPID','OBJNR']

PRJ_New_dataframe = Historic_data['PRJ'][PRJ_id_columns]
FIN_New_dataframe = Historic_data['FIN'][FIN_id_columns]

PRJ_New_dataframe = PRJ_New_dataframe.add_prefix('PRJ-')
FIN_New_dataframe = FIN_New_dataframe.add_prefix('FIN-')

# print(PRJ_New_dataframe)
# print(FIN_New_dataframe)

#PRJ_New_dataframe
PROJ_md_field_values = sdv_metadata_md[sdv_metadata_md['Table_name']=='PROJ']
PRPS_md_field_values = sdv_metadata_md[sdv_metadata_md['Table_name']=='PRPS']
IHPA_md_field_values = sdv_metadata_md[sdv_metadata_md['Table_name']=='IHPA']
ZTCTC_PROJ_AU_md_field_values = sdv_metadata_md[sdv_metadata_md['Table_name']=='ZTCTC_PROJ_AU']
ZTCTC_PROJ_GLB_md_field_values = sdv_metadata_md[sdv_metadata_md['Table_name']=='ZTCTC_PROJ_GLB']

# print(PRPS_md_field_values)
PROJ_md_field_values_list = PROJ_md_field_values['Field_name'].tolist()
PRPS_md_field_values_list = PRPS_md_field_values['Field_name'].tolist()
IHPA_md_field_values_list = IHPA_md_field_values['Field_name'].tolist()
ZTCTC_PROJ_AU_md_field_values_list = ZTCTC_PROJ_AU_md_field_values['Field_name'].tolist()
ZTCTC_PROJ_GLB_md_field_values_list = ZTCTC_PROJ_GLB_md_field_values['Field_name'].tolist()

historic_data_proj = Historic_data['PRJ'][PROJ_md_field_values_list]
historic_data_proj=historic_data_proj.add_prefix('PRJ-PROJ-')
historic_data_proj=historic_data_proj.add_suffix('-S')

historic_data_prps = Historic_data['PRJ'][PRPS_md_field_values_list]

historic_data_prps = historic_data_prps.add_prefix('PRJ-PRPS-')
historic_data_prps = historic_data_prps.add_suffix('-S')

historic_data_ihpa = Historic_data['PRJ'][IHPA_md_field_values_list]
historic_data_ihpa = historic_data_ihpa.add_prefix('PRJ-IHPA-')
historic_data_ihpa = historic_data_ihpa.add_suffix('-S')

historic_data_ZTCTC_PROJ_AU = Historic_data['PRJ'][ZTCTC_PROJ_AU_md_field_values_list]

historic_data_ZTCTC_PROJ_AU = historic_data_ZTCTC_PROJ_AU.add_prefix('PRJ-ZTCTC_PROJ_AU-')
historic_data_ZTCTC_PROJ_AU = historic_data_ZTCTC_PROJ_AU.add_suffix('-S')

historic_data_ZTCTC_PROJ_GLB = Historic_data['PRJ'][ZTCTC_PROJ_GLB_md_field_values_list]

historic_data_ZTCTC_PROJ_GLB = historic_data_ZTCTC_PROJ_GLB.add_prefix('PRJ-ZTCTC_PROJ_GLB-')
historic_data_ZTCTC_PROJ_GLB = historic_data_ZTCTC_PROJ_GLB.add_suffix('-S')
# print('historic_data_proj',historic_data_proj.columns)
# print('historic_data_prps',historic_data_prps.columns)
# print('historic_data_ihpa',historic_data_ihpa.columns)
# print('historic_data_ZTCTC_PROJ_AU',historic_data_ZTCTC_PROJ_AU.columns)
# print('historic_data_ZTCTC_PROJ_GLB',historic_data_ZTCTC_PROJ_GLB.columns)
historic_data_ihpa = historic_data_ihpa.loc[:,~historic_data_ihpa.columns.duplicated()]
historic_data_prps = historic_data_prps.loc[:,~historic_data_prps.columns.duplicated()]
historic_data_ZTCTC_PROJ_GLB = historic_data_ZTCTC_PROJ_GLB.loc[:,~historic_data_ZTCTC_PROJ_GLB.columns.duplicated()]
historic_data_ZTCTC_PROJ_AU = historic_data_ZTCTC_PROJ_AU.loc[:,~historic_data_ZTCTC_PROJ_AU.columns.duplicated()]
# print(historic_data_proj)

PRJ_New_dataframe = pd.concat([PRJ_New_dataframe,historic_data_proj,historic_data_prps,historic_data_ihpa,historic_data_ZTCTC_PROJ_AU,historic_data_ZTCTC_PROJ_GLB],axis=1)

#print(PRJ_New_dataframe.columns)

#FIN_New_dataframe

CPD_D_MP_HDR_md_field_values = sdv_metadata_md[sdv_metadata_md['Table_name']=='/CPD/D_MP_HDR']
CPD_D_MP_MEMBER_md_field_values = sdv_metadata_md[sdv_metadata_md['Table_name']=='/CPD/D_MP_MEMBER']

CPD_D_MP_HDR_md_field_values_list = CPD_D_MP_HDR_md_field_values['Field_name'].tolist()
CPD_D_MP_MEMBER_md_field_values_list = CPD_D_MP_MEMBER_md_field_values['Field_name'].tolist()


historic_data_CPD_D_MP_HDR = Historic_data['FIN'][CPD_D_MP_HDR_md_field_values_list]
historic_data_CPD_D_MP_HDR=historic_data_CPD_D_MP_HDR.add_prefix('FIN-/CPD/D_MP_HDR-')
historic_data_CPD_D_MP_HDR=historic_data_CPD_D_MP_HDR.add_suffix('-C')


historic_data_CPD_D_MP_MEMBER = Historic_data['FIN'][CPD_D_MP_MEMBER_md_field_values_list]
historic_data_CPD_D_MP_MEMBER=historic_data_CPD_D_MP_MEMBER.add_prefix('FIN-/CPD/D_MP_MEMBER-')
historic_data_CPD_D_MP_MEMBER=historic_data_CPD_D_MP_MEMBER.add_suffix('-C')


historic_data_CPD_D_MP_HDR = historic_data_CPD_D_MP_HDR.loc[:,~historic_data_CPD_D_MP_HDR.columns.duplicated()]
historic_data_CPD_D_MP_MEMBER = historic_data_CPD_D_MP_MEMBER.loc[:,~historic_data_CPD_D_MP_MEMBER.columns.duplicated()]



FIN_New_dataframe = pd.concat([FIN_New_dataframe,historic_data_CPD_D_MP_HDR,historic_data_CPD_D_MP_MEMBER],axis=1)

print(FIN_New_dataframe.columns)

FIN_New_dataframe.to_excel(r'C:\Users\vamsikkrishna\PycharmProjects\sdg_sdv\Engagement_training_directory\FIN_New_dataframe.xlsx')
print('FIN_new_dataframe')
pivot_table = pd.DataFrame([])
parvw_list = ['Z3','Z4','Z6','Z8','Z1','Z2','Z9','Y3']
eng_prj_ihpa = PRJ_New_dataframe[['PRJ-POSID','PRJ-IHPA-PARVW-S','PRJ-IHPA-PARNR-S']]
eng_prj_ihpa_filter = eng_prj_ihpa[eng_prj_ihpa['PRJ-IHPA-PARVW-S'].isin(parvw_list)]

unique_posid = eng_prj_ihpa['PRJ-POSID'].unique().tolist()

for i in unique_posid:
    df_temp= eng_prj_ihpa_filter.loc[eng_prj_ihpa['PRJ-POSID']==i,]
    table = pd.pivot_table(df_temp,values='PRJ-IHPA-PARNR-S',index=['PRJ-POSID'],columns= ['PRJ-IHPA-PARVW-S'],aggfunc='first').reset_index()
    pivot_table = pd.concat([pivot_table,table],axis=0)


#print(pivot_table)

PRJ_New_dataframe = PRJ_New_dataframe.merge(pivot_table,how = 'inner',left_on ='PRJ-POSID',right_on = 'PRJ-POSID' ).reset_index()

PRJ_New_dataframe.to_excel(r'C:\Users\vamsikkrishna\PycharmProjects\sdg_sdv\Engagement_training_directory\PRJ_New_dataframe.xlsx')

print(PRJ_New_dataframe)

PRJ_FIN_merge = PRJ_New_dataframe.merge(FIN_New_dataframe,how = 'inner',left_on ='PRJ-PSPNR',right_on = 'FIN-PSPNR')

PRJ_FIN_merge = PRJ_FIN_merge[Masterdata_columns]

float_columns = PRJ_FIN_merge.select_dtypes('float64').columns.tolist()

fill_na_value = 444444

for col in float_columns:
  PRJ_FIN_merge[col]=PRJ_FIN_merge[col].fillna(fill_na_value,).astype(int)

PRJ_FIN_merge.replace(fill_na_value,np.nan,inplace = True)
PRJ_FIN_merge.replace(np.nan,'BLANK_VALUES')



metadata_Master = SingleTableMetadata()

for i in Masterdata_columns:

  metadata_Master.update_column(
        column_name= i,
        sdtype='categorical'
    )


master_data_constraint = {
    'constraint_class': 'FixedCombinations',
    'constraint_parameters': {
        'column_names': Masterdata_columns
    }
}


synthesizer_Master = GaussianCopulaSynthesizer(metadata_Master)
synthesizer_Master.add_constraints(constraints=[master_data_constraint])
synthesizer_Master.fit(PRJ_FIN_merge)

synthesizer_Master.save(Save_pickle_dict['Engagement_Master_data_pickle_file'])


###############Backend_derived###############################################

sdv_metadata_bd = sdv_metadata[sdv_metadata['Rule_indicator']=='BD']

sdv_metadata_bd['column_name'] = sdv_metadata_bd['Sub_process_area']+'-'+sdv_metadata_bd['Table_name']+'-'+sdv_metadata_bd['Field_name']+'-'+sdv_metadata_bd['Output_file']

Backend_derived_columns = sdv_metadata_bd['column_name'].tolist()
print(Backend_derived_columns)

ENG_backend_derived = pd.DataFrame([],columns=Backend_derived_columns)

Backend_derived_value=['Backend_derived']*100
for i in ENG_backend_derived.columns.tolist():
  ENG_backend_derived[i]= Backend_derived_value


sdv_metadata_dv = sdv_metadata[sdv_metadata['Rule_indicator']=='DV']

sdv_metadata_dv['column_name'] = sdv_metadata_dv['Sub_process_area']+'-'+sdv_metadata_dv['Table_name']+'-'+sdv_metadata_dv['Field_name']+'-'+sdv_metadata_dv['Output_file']

Default_value_columns = sdv_metadata_dv['column_name'].tolist()

Default_value_columns_values = sdv_metadata_dv['Field_value'].tolist()

ENG_Default_values = pd.DataFrame([],columns=Default_value_columns)

for i in range(len(Default_value_columns)):
  d= [Default_value_columns_values[i]]*100
  ENG_Default_values[Default_value_columns[i]]=d



metadata_backend = SingleTableMetadata()
metadata_default = SingleTableMetadata()

metadata_backend.detect_from_dataframe(ENG_backend_derived)

synthesizer_backend_derived = GaussianCopulaSynthesizer(metadata_backend)
synthesizer_backend_derived.fit(ENG_backend_derived)

metadata_default.detect_from_dataframe(ENG_Default_values)
print(metadata_default)

synthesizer_default_values = GaussianCopulaSynthesizer(metadata_default)
synthesizer_default_values.fit(ENG_Default_values)

synthesizer_backend_derived.save(Save_pickle_dict['Engagement_Backend_Derived_Pickle_file'])
synthesizer_default_values.save(Save_pickle_dict['Engagement_Default_values_pickle_file'])
sdv_metadata_txt = sdv_metadata[sdv_metadata['Rule_indicator']=='TXT']
sdv_metadata_txt['column_name'] = sdv_metadata_txt['Sub_process_area']+'-'+sdv_metadata_txt['Table_name']+'-'+sdv_metadata_txt['Field_name']+'-'+sdv_metadata_txt['Output_file']

Text_value_columns = sdv_metadata_txt['column_name'].tolist()

############ TXT words #############


TXT_words_list =[]
for index,row in TXT_words.iterrows():
  k= row['TXT_words']
  TXT_words_list_temp = k.split(',')
  TXT_words_list.extend(TXT_words_list_temp)

fake= Faker()

sentence_list = []

for i in range(10000):
  sentence_list.append(fake.sentence(ext_word_list=TXT_words_list))

text_training_data = pd.DataFrame([])
for index,row in sdv_metadata_txt.iterrows():
    parameter_value = int(row['Field_value'].split(',')[0])
    text_training_data[row['column_name']] = sentence_list[:parameter_value]

metadata_txt = SingleTableMetadata()
metadata_txt.detect_from_dataframe(text_training_data)

Text_data_constraint = {
    'constraint_class': 'FixedCombinations',
    'constraint_parameters': {
        'column_names': Text_value_columns
    }
}

synthesizer_text_values = GaussianCopulaSynthesizer(metadata_txt)
synthesizer_text_values.add_constraints(constraints=[Text_data_constraint])
synthesizer_text_values.fit(text_training_data)
synthesizer_text_values.save(Save_pickle_dict['Engagement_Text_data_pickle_file'])
print("All Pickle files generated")
