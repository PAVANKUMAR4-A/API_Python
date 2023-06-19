import pandas as pd
import numpy as np
import json

class Autogen_variable_rule_dep_data_gen():

    def Rule_Dependency_transformations(self,ENG_RLDP_df, parameter_value, json_ui, concat_dataframe, Historic_data_locations,
                Data_dependency_df):
        print("Rule dependency transformations")

        extracted_json = json.loads(json_ui)

        result_df = pd.DataFrame([])
        concat_dataframe_temp =concat_dataframe.copy()
        concat_dataframe_temp.to_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\concat_dataframe_tempbefore.xlsx')
        data_dependency = Data_dependency_df
        #print(data_dependency)
        try:
            for index, row in Data_dependency_df.iterrows():
                # print(row['Condition'])
                if row['Condition'].lower() == 'EQUALITY'.lower():
                    print('equality', 'target', row['Target_field'], 'source', row['Source_field'])
                    concat_dataframe_temp[row['Target_field']] = concat_dataframe_temp[row['Source_field']]
                    # print(concat_dataframe_temp[row['Target_field']])
                    concat_dataframe_temp.to_excel(
                        r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\concat_dataframe_tempafter.xlsx')

                elif row['Condition'].lower() == 'CONCAT'.lower():
                    print('concat', 'target', row['Target_field'], 'source', row['Source_field'])
                    print(concat_dataframe_temp[row['Source_field']])
                    #print(concat_dataframe_temp['FIN-/CPD/D_MP_HDR-DB_KEY-C'])
                    concat_dataframe_temp[row['Target_field']] = concat_dataframe_temp[row['Source_field']]+concat_dataframe_temp[row['Target_field']]
                    # print(concat_dataframe_temp[row['Target_field']]
                    print("result", concat_dataframe_temp[row['Target_field']])

                elif row['Condition'].lower() == 'CONDITIONASSIGN'.lower():
                    print("conditionassign")
                    condition_value_split = row['Condition_value'].split(',')
                    condition_name = condition_value_split[0].split('-')[1]
                    condition_value_assign = condition_value_split[1].split('-')[1]
                    concat_dataframe_temp.loc[:, row['Target_field']] = 'BLANK_VALUES'
                    #concat_dataframe_temp
                    print("created new column ",row['Target_field'],concat_dataframe_temp[row['Target_field']])
                    concat_dataframe_temp.loc[concat_dataframe_temp[row['Source_field']].str.contains(condition_name), row['Target_field']] = condition_value_assign


                elif row['Condition'].lower() == 'REPLACE'.lower():
                    print("conditionassign")

                    replace_values = row['Target_field'].split(',')
                    for val in replace_values:
                        concat_dataframe_temp.replace(val,np.nan,inplace=True)


                elif row['Condition'].lower() == 'UIASSIGN'.lower():
                    print("UIASSIGN")

                    condition_value = row['Condition_value'].split('-')[1]

                    if condition_value.lower() == 'equal'.lower():
                        if str(extracted_json[row['Source_field']]) == str(0):
                            print("Noclientselected")
                        else:
                            condition_value_split = row['Condition_value'].split(',')
                            Target_fields_list = row['Target_field'].split(',')

                            for col in Target_fields_list:
                                concat_dataframe_temp[col] = extracted_json[row['Source_field']]
                            concat_dataframe_temp.to_excel(
                                r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\sample_synthetic_master_uiassign.xlsx')

                    elif condition_value.lower() == 'newequal'.lower():
                        if str(extracted_json[row['Source_field']]) == str(0):
                            print("Noenvironmentselected")
                            value_assigned = '30'
                        else:
                            value_assigned = str(extracted_json[row['Source_field']])
                        condition_value_split = row['Condition_value'].split(',')
                        Target_fields_list = row['Target_field'].split(',')

                        for col in Target_fields_list:
                            concat_dataframe_temp[col] = value_assigned
                        concat_dataframe_temp.to_excel(
                            r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\sample_synthetic_master_uiassign_newequal.xlsx')




                elif row['Condition'].lower() == 'MASTERTRANSFORM'.lower():
                    print("MASTERTRANSFORM")
                    condition_value_split = row['Condition_value'].split(',')
                    condition_name = condition_value_split[0].split('-')[1]
                    condition_value_assign_split = condition_value_split[1].split('-')[1]
                    condition_value_assign = condition_value_assign_split.split('^')

                    target_value_split = row['Target_field'].split(',')
                    var_name = target_value_split[1]
                    value_name = target_value_split[0]

                    df = pd.melt(concat_dataframe_temp, id_vars=row['Source_field'], value_vars=condition_value_assign,
                                 var_name=var_name, value_name=value_name)
                    g = df.merge(concat_dataframe_temp, how=condition_name, on=row['Source_field'])
                    concat_dataframe_temp = g
                    val_vars = condition_value_assign
                    for i in val_vars:
                        del concat_dataframe_temp[i]
                    concat_dataframe_temp.to_excel(
                        r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\sample_synthetic_master_transform.xlsx')



                else:
                    print("no condition")

        except Exception as e:
            print('exceptione',e)
            #return (e)

        print("after")
        concat_dataframe_temp.to_excel(r'C:\Users\vamsikkrishna\PycharmProjects\pythonProject1\sample_synthetic\concat_dataframe_tempafter.xlsx')
        #print(concat_dataframe_temp)
        return(concat_dataframe_temp)


