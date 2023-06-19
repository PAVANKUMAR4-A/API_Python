from sdv.single_table import GaussianCopulaSynthesizer
from sdv.sampling import Condition
#from sdv
import json
import pandas as pd
from sdv.sampling import Condition
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata
from sdv.constraints import FixedCombinations


Pickle_file_locations=pd.read_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\Engagement_training_config_file\Engagement_training_config_file.xlsx',sheet_name='Pickle_file_locations')

Pikcle_file_description = 'Engagement_Default_values_pickle_file'

for index,row in Pickle_file_locations.iterrows():
    if row['Pikcle_file_description'].lower()==Pikcle_file_description.lower():
        saved_location = row['Saved_location']
        print(saved_location)


saved_location=r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\Pickle_file_locations\Engagement_Backend_Derived_Pickle_file\Engagement_Backend_Derived_Pickle_file.pkl'
synthesizer = GaussianCopulaSynthesizer.load(
            filepath=saved_location
        )


# suite_guests_with_rewards = Condition(
#     num_rows=250,
#     column_values={'room_type': 'SUITE', 'has_rewards': True}
# )
#
# suite_guests_without_rewards = Condition(
#     num_rows=250,
#     column_values={'room_type': 'SUITE', 'has_rewards': False}
# )

synthetic_data = synthesizer.sample(num_rows=100)
print(synthetic_data)