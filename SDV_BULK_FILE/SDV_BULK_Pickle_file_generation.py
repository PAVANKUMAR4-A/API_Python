import pandas as pd
import numpy as np
from faker import Faker
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata
from sdv.constraints import FixedCombinations
from SDV_Class_files import Pickle_file_config_file

Bulk_data_config_file = pd.read_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\BULK_CONFIG_FILE\Engagement_training_config_file.xlsx',sheet_name='SDV_BULK')
Bulk_pickle_file_locations = pd.read_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\BULK_CONFIG_FILE\Engagement_training_config_file.xlsx',sheet_name='BULK_Pickle_file_locations')
TXT_words = pd.read_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\BULK_CONFIG_FILE\Engagement_training_config_file.xlsx',sheet_name='TXT_words')
############## retreiving Backend_derived_values #################

Bulk_Backend_derived_df = pd.DataFrame([])
Bulk_data_Backend_derived = Bulk_data_config_file[Bulk_data_config_file['Rule_indicator']=='BD']
Bulk_data_Backend_derived_columns = Bulk_data_Backend_derived['Template_field_name'].tolist()

pickle_file_name = Bulk_data_Backend_derived['Pikcle_file_description'].unique().tolist()[0]
print(pickle_file_name)

Bulk_pickle_file_locations_saved = Bulk_pickle_file_locations[Bulk_pickle_file_locations['Pikcle_file_description']==pickle_file_name]['Saved_location'].tolist()[0]

#Bulk_pickle_file_locations['Saved_location']

fill_value = ['Backend_derived']*100

for col in Bulk_data_Backend_derived_columns :
    Bulk_Backend_derived_df[col] = fill_value

metadata_backend_bulk = SingleTableMetadata()
metadata_backend_bulk.detect_from_dataframe(Bulk_Backend_derived_df)
print(metadata_backend_bulk)
backend_derived_bulk_synthesizer = GaussianCopulaSynthesizer(metadata_backend_bulk)
backend_derived_bulk_synthesizer.fit(Bulk_Backend_derived_df)
synthetic_data = backend_derived_bulk_synthesizer.sample(num_rows=10)
print(synthetic_data.head())
backend_derived_bulk_synthesizer.save(Bulk_pickle_file_locations_saved)

##################### retreive Default_values ##################

Bulk_Default_df = pd.DataFrame([])
Bulk_data_Default = Bulk_data_config_file[Bulk_data_config_file['Rule_indicator']=='DV']
Bulk_data_default_columns = Bulk_data_Default['Template_field_name'].tolist()
Bulk_data_default_values = Bulk_data_Default['Field_value'].tolist()
pickle_file_name = Bulk_data_Default['Pikcle_file_description'].unique().tolist()[0]
print(Bulk_data_default_columns)

Bulk_pickle_file_locations_saved = Bulk_pickle_file_locations[Bulk_pickle_file_locations['Pikcle_file_description']==pickle_file_name]['Saved_location'].tolist()[0]

for index,row in Bulk_data_Default.iterrows():

    default_value = [row['Field_value']]*100
    Bulk_Default_df[row['Template_field_name']] = default_value
#print(Bulk_Default_df)

metadata_default_bulk = SingleTableMetadata()
metadata_default_bulk.detect_from_dataframe(Bulk_Default_df)

for i in Bulk_data_default_columns:

  metadata_default_bulk.update_column(
        column_name= i,
        sdtype='categorical'
    )

from sdv.single_table import GaussianCopulaSynthesizer

default_bulk_synthesizer = GaussianCopulaSynthesizer(metadata_default_bulk)
default_bulk_synthesizer.fit(Bulk_Default_df)
synthetic_data = default_bulk_synthesizer.sample(num_rows=10)
print(synthetic_data.head())
default_bulk_synthesizer.save(Bulk_pickle_file_locations_saved)


###################### retreiving Text fields ##############


text_df = pd.DataFrame([])
Bulk_TXT_data = Bulk_data_config_file[Bulk_data_config_file['Rule_indicator']=='TXT']
Bulk_TXT_data_columns = Bulk_TXT_data['Template_field_name'].tolist()
pickle_file_name = Bulk_TXT_data['Pikcle_file_description'].unique().tolist()[0]

Bulk_pickle_file_locations_saved = Bulk_pickle_file_locations[Bulk_pickle_file_locations['Pikcle_file_description']==pickle_file_name]['Saved_location'].tolist()[0]



TXT_words_list =[]
for index,row in TXT_words.iterrows():
  k= row['TXT_words']
  TXT_words_list_temp = k.split(',')
  TXT_words_list.extend(TXT_words_list_temp)

fake= Faker()

sentence_list = []

for i in range(10000):
  sentence_list.append(fake.sentence(ext_word_list=TXT_words_list))

#print(sentence_list)
text_training_data = pd.DataFrame([])
for index,row in Bulk_TXT_data.iterrows():
    parameter_value = int(row['Field_value'].split(',')[0])
    text_training_data[row['Template_field_name']] = sentence_list
    text_training_data[row['Template_field_name']] = text_training_data[row['Template_field_name']].str[:parameter_value]

metadata_txt = SingleTableMetadata()
metadata_txt.detect_from_dataframe(text_training_data)

Text_data_constraint = {
    'constraint_class': 'FixedCombinations',
    'constraint_parameters': {
        'column_names': Bulk_TXT_data_columns
    }
}

synthesizer_text_values = GaussianCopulaSynthesizer(metadata_txt)
synthesizer_text_values.add_constraints(constraints=[Text_data_constraint])
synthesizer_text_values.fit(text_training_data)
synthetic_data = synthesizer_text_values.sample(num_rows=200)
#synthetic_data.to_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\txtsynthetic.xlsx')
synthesizer_text_values.save(Bulk_pickle_file_locations_saved)


################### retreiving Master data ###################################