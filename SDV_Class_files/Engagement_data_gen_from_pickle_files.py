import pandas as pd
import numpy as np
import json
import datetime
import random
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata
from sdv.constraints import FixedCombinations

class Engagement_data_from_pickle_file():

    def Engagement_Master_data_from_pickle_file(self,Process_area,json_ui,sdv_metadata,Historic_data_locations,Pickle_file_locations):
        print("Master_data_pickle_file")
