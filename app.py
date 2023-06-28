import json
import requests
import numpy as np
import pandas as pd
import pyodbc
from flask import Flask, request,render_template,send_file,jsonify
from SDV_BULK_API_FILE.Header_DB import Header_DB_Class
import json
from urllib.parse import urlencode
#from SDV_BULK_FILE.SDV_BULK_Driver_file import Bulk_Driver
from SDV_BULK_API_FILE.SDV_BULK_UPDATED_file_API import Bulk_Driver
from SDV_BULK_API_FILE.SDV_BULK_GET_Data_Display import Generated_data_display
from SDV_BULK_API_FILE.DB_data import DB_Updates
from datetime import datetime

app = Flask(__name__,template_folder='templates')

input_dict= {}
dat_frame = pd.DataFrame([])



try:

    @app.route("/API/1.0/getProcLastDataSetsList", methods=['GET'])
    def Get_ProcLastDataSets_List():

        process_area = request.args.get('ProcessArea')


        from_Date = datetime.strptime(request.args.get('FromDate'),'%m%d%Y').date()
        to_Date = datetime.strptime(request.args.get('ToDate'),'%m%d%Y').date()


        conn_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Users\pavankumar4\Documents\Database1.accdb;'
        conn = pyodbc.connect(conn_string)

        # cursor = conn.cursor()
        sql_query = "SELECT *, Created_On FROM Dataset"

        # Execute the SQL query and fetch the results
        df = pd.read_sql_query(sql_query, conn)

        conn.close()

        # Extract date from 'Created_On' column and create a new column with formatted date
        df['Formatted_Date'] = pd.to_datetime(df['Created_On']).dt.strftime('%m%d%Y')


        filtered_df = df[(df['Formatted_Date'] >= from_Date.strftime('%m%d%Y')) &
                         (df['Formatted_Date'] <= to_Date.strftime('%m%d%Y'))]

        filtered_df.rename(columns={"DataSet_GUID":"id"}, inplace=True)
        filtered_df.drop(['DataSet_Table', 'Changed_By','Changed_On','Formatted_Date','Target_system'], axis=1, inplace=True)


        output_dict = filtered_df.to_dict('records')


        final_dict = {"lastDataSets": output_dict}

        return final_dict




    @app.route("/API/1.0/getUserInputQuesList", methods=['GET'])
    def get_User_Input_QuesList():
        conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\Users\pavankumar4\Documents\Database1.accdb;'

        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        process_area = request.args.get('ProcessArea')


        # Retrieve data from the Access database
        cursor.execute("SELECT * FROM UserInputQuestions2",)
        rows = cursor.fetchall()
        connection.close()

        # Format data as JSON
        user_input_ques_list = []

        params = {
            'CountryKey': 'str',
            'entity': 'int'

        }
        for row in rows:

            if row.APIRequest is not None:
                user_input_ques_list.append({
                "fieldName": row.FieldName,
                "quesType": row.Question_Type,
                "sequence": int(row.Sequence),
                # "Dependent sequence": row.DependentSeq,
                "question": row.Question,
                #"dataType": row.Datatype,
                "value": row.FieldValue,
                "apiRequest":f"http://127.0.0.1:5000/API/1.0/{row.APIRequest}?{urlencode(params)}",

                "type": row.inputType

                })
            else:
                continue



        return jsonify({"userInputQues": user_input_ques_list})

    @app.route('/API/1.0/getPartnerTypeList', methods=['GET'])
    def Get_PartnerType_List():
        Database_object = DB_Updates()
        df = Database_object.Retrieve_dropdown()

        temp1_df = df['Field_values'].str.split(',', expand=True)

        total_columns = len(temp1_df.columns)

        df = pd.DataFrame()
        for i in range(total_columns):
            if i >= 4:
                data = temp1_df[i].str.split('@', expand=True)

                df =pd.concat([df,data],axis=0)


        df.rename(columns={0: 'partnerTypeId', 1: 'partnerTypeName', 2: 'ZZ_CLIENT', 3: 'partnerName'}, inplace=True)
        df.drop(['ZZ_CLIENT', 'partnerName'],axis=1, inplace=True)

        # Remove duplicate entries from the DataFrame
        df_unique = df.drop_duplicates().reset_index(drop=True)

        output_dict = df_unique.to_dict('records')

        final_dict = {"partnerTypeSet": output_dict}

        return final_dict


    @app.route('/API/1.0/getGeoList', methods=['GET'])
    def get_GeoList():

        Database_object = DB_Updates()
        df = Database_object.Retrieve_dropdown()
        temp1_df = df['Field_values'].str.split(',', expand=True)
        temp2_df = temp1_df[0].str.split('@', expand=True)
        temp2_df.rename(columns={0: 'countryKey', 1: 'countryName'}, inplace=True)
        temp2_df = temp2_df.drop_duplicates().reset_index(drop=True)
        temp2_df_list = temp2_df.to_dict('records')
        # response = {'geographySet': temp2_df_list}
        # return response

        response = {
            "response": [
                {
                    "name": "OK",
                    "originalRequest": {
                        "method": "GET",
                        "header": [
                            {
                                "key": "Accept",
                                "value": "application/json"
                            }
                        ],
                        "url": {
                            "raw": "{{baseUrl}}/getGeoList",
                            "host": [
                                "{{baseUrl}}"
                            ],
                            "path": [
                                "getGeoList"
                            ]
                        }
                    },
                    "status": "OK",
                    "code": 200,
                    "_postman_previewlanguage": "json",
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "cookie": [],
                    "body": {
                        "geographySet": [
                            {"key": record["countryKey"], "label": record["countryName"]} for record in temp2_df_list
                        ]
                    }
                }
            ]
        }

        return response


    @app.route('/API/1.0/getEntityList', methods=['GET'])
    def get_EntityList():
        Database_object = DB_Updates()
        df = Database_object.Retrieve_dropdown()

        countryKey = request.args.get('CountryKey')


        df = df[df['Field_values'].str.contains(countryKey)]

        temp1_df = df['Field_values'].str.split(',', expand=True)
        temp2_df = temp1_df[1].str.split('@', expand=True)
        temp2_df.rename(columns={0: 'entity', 1: 'entityName'}, inplace=True)
        temp2_df = temp2_df.drop_duplicates().reset_index(drop=True)
        temp2_df['countryKey'] = countryKey
        temp2_df_list = temp2_df.to_dict('records')
        # response = {'entitySet': temp2_df_list}
        # return response

        response = {
            "response": [
                {
                    "name": "OK",
                    "originalRequest": {
                        "method": "GET",
                        "header": [
                            {
                                "key": "Accept",
                                "value": "application/json"
                            }
                        ],
                        "url": {
                            "raw": "{{baseUrl}}/getEntityList?countryKey=" + countryKey,
                            "host": [
                                "{{baseUrl}}"
                            ],
                            "path": [
                                "getEntityList"
                            ],
                            "query": [
                                {
                                    "key": "countryKey",
                                    "value": countryKey,
                                    "description": "(Required) Country Key"
                                }
                            ]
                        }
                    },
                    "status": "OK",
                    "code": 200,
                    "_postman_previewlanguage": "json",
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "cookie": [],
                    "body": {
                        "entitySet": [
                            {
                                "countryKey": record["countryKey"],
                                "entity": record["entity"],
                                "entityName": record["entityName"]
                            } for record in temp2_df_list
                        ]
                    }
                }
            ]
        }

        return response


    @app.route('/API/1.0/getClientList', methods=['GET'])
    def Get_ClientList():
        Database_object = DB_Updates()
        df = Database_object.Retrieve_dropdown()


        countryKey = request.args.get('CountryKey')

        entity = request.args.get('entity')
        df = df[df['Field_values'].str.contains(countryKey)]
        df = df[df['Field_values'].str.contains(entity)]

        temp1_df = df['Field_values'].str.split(',', expand=True)
        temp2_df = temp1_df[2].str.split('@', expand=True)
        temp2_df.rename(columns={0: 'countryKey', 1: 'clientNum'}, inplace=True)
        temp2_df = temp2_df.drop_duplicates().reset_index(drop=True)
        temp2_df['countryKey'] = countryKey
        temp2_df_list = temp2_df.to_dict('records')
        response = {'clientSet': temp2_df_list}
        return response


    @app.route('/API/1.0/getEngmtTypeList', methods=['GET'])
    def Get_Engagement_typeList():
        Database_object = DB_Updates()
        df = Database_object.Retrieve_dropdown()
        countryKey = request.args.get('CountryKey')
        print(countryKey)
        entity = request.args.get('entity')
        print(type(entity), entity)
        if '-' in entity:
            entity_list = entity.split('-')
            entity = "|".join(entity_list)

        df = df[df['Field_values'].str.contains(countryKey)]

        df = df[df['Field_values'].str.contains(str(entity))]

        temp1_df = df['Field_values'].str.split(',', expand=True)

        temp2_df = temp1_df[3].str.split('@', expand=True)

        temp2_df.rename(columns={0: 'engTypeIdNum', 1: 'projectType', 2: 'engTypeId', 3: 'engTypeName', 4: 'BEZEI'},
                        inplace=True)

        temp2_df = temp2_df.drop_duplicates().reset_index(drop=True)
        temp2_df_list = temp2_df.to_dict('records')

        response = {'engTypeSet': temp2_df_list}

        return response


    @app.route('/API/1.0/getPartnerNumbers', methods=['GET'])
    def Get_PartnerNum_List():
        Database_object = DB_Updates()
        df = Database_object.Retrieve_dropdown()
        partner_dict_map = {'Z3': 5, 'Z4': 4, 'Z7': 6, 'Z6': 7}
        countryKey = request.args.get('CountryKey')
        print(countryKey)
        entity = request.args.get('entity')
        print(type(entity), entity)
        if '-' in entity:
            entity_list = entity.split('-')
            entity = "|".join(entity_list)
        partnerType = request.args.get('partnerType')
        print(type(partnerType), partnerType)
        df = df[df['Field_values'].str.contains(countryKey)]
        print("country", df)
        df = df[df['Field_values'].str.contains(str(entity))]
        print("entity", df)
        df = df[df['Field_values'].str.contains(str(partnerType))]
        print("partnerType", df)
        temp1_df = df['Field_values'].str.split(',', expand=True)
        print('temp1', temp1_df)
        temp2_df = temp1_df[partner_dict_map[partnerType]].str.split('@', expand=True)
        print('temp2before', temp2_df)
        temp2_df.rename(columns={0: 'partnerTypeId', 1: 'partnerTypeIdDes', 2: 'partnerNum', 3: 'partnerName'},
                        inplace=True)
        print('temp2after', temp2_df)
        temp2_df = temp2_df.drop_duplicates().reset_index(drop=True)
        temp2_df_list = temp2_df.to_dict('records')
        print(temp2_df_list)
        response = {'partnerNumSet': temp2_df_list}
        print("response", response)
        return response


    @app.route("/API/1.0/DataGenResponseSet", methods=['GET'])
    def data_gen_response_set():
        matching_data = {
            "Entity": "PBUKR",
            "Start Date": "PLFEZ",
            "End Date": "PLSEZ",
            "Client": "ZZ_CLIENT",
            "Requester E-Mail": "Email",
            "Engagement Type": "PRART",
            "Eng Partner": "Z3",
            "Eng Manager": "Z4"
        }

        search_param1 = request.args.get('DataSet_GUID')
        search_param2 = request.args.get('DataSet_Name')


        display_object = Generated_data_display()
        response_display = display_object.Screen_Data_display(dat_frame, input_dict)
        print('Actual response', response_display)

        output_columns = response_display.columns

        response_display.to_excel(r'sample_synthetic/output_file2.xlsx', index=False)
        response_display = pd.read_excel(r'sample_synthetic/output_file2.xlsx')
        response_display = response_display.applymap(lambda x: x.astype(int) if isinstance(x, np.int64) else x)

        header_info = {
            "processAreaId": input_dict['ProcessAreaId'],
            "dataSetName": input_dict["DataSetName"],
            "TargetSys": input_dict["TargetSys"],
            "CountryKey": input_dict['CountryKey'],
            # "numOfRecords": input_dict['NumOfRecords']
        }

        if search_param1 and search_param2:

            df = pd.read_excel(r'sample_synthetic/DB_Tables.xlsx', sheet_name='DataSet_ENG')
            response_display = df[(df['DataSet_GUID'] == search_param1) & (df['DataSet_Name'] == search_param2)]
            response_display = response_display[output_columns]
            print('Inside Search data df:', response_display, type(response_display))
            response_display.to_excel(r'sample_synthetic/searched_data.xlsx', index=False)

            response_display = pd.read_excel(r'sample_synthetic/searched_data.xlsx')
        # Pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        if search_param1 and search_param2:
            total_records = len(response_display)
            total_pages = (total_records + per_page - 1) // per_page

            # Calculate start and end index for pagination
            start_index = (page - 1) * per_page
            end_index = start_index + per_page

            paginated_data = response_display.iloc[start_index:end_index]

            # Apply pagination to inputSet
            input_set = []

            for row_index, row in response_display.iterrows():
                print('inside search row', row)

                print(f'inside search ,Start index:{start_index} End index:{end_index}  and row_index:{row_index}')
                if row_index >= start_index and row_index <end_index:
                    for col_index, value in enumerate(row):
                        print('inside search col and col value', col_index, value)
                        if response_display.columns[col_index] in matching_data:
                            print('inside search Inside if ', response_display.columns[col_index])
                            input_set.append({
                                "fieldName": matching_data[response_display.columns[col_index]],
                                "fieldDesc": response_display.columns[col_index],
                                "fieldValue": response_display.iloc[row_index, col_index],
                                'fieldIndex': row_index +1
                            })

                    print(f"All values in Row {row_index} processed.")

            # Create pagination metadata
            pagination_info = {
                "page": page,
                "per_page": per_page,
                "total_records": total_records,
                "total_pages": total_pages
            }

            input_set_data = input_set


            input_set_df = pd.DataFrame(input_set)
            if 'fieldValue' in input_set_df.columns:
                df = pd.pivot_table(input_set_df, index='fieldIndex', columns='fieldDesc', values='fieldValue',
                                    aggfunc=lambda x: x)
                df = df.reset_index(drop=True)
                # df['Index_position'] = range(start_index + 1, end_index + 1)
                columns = [col for col in df.columns if col != 'Index_position']
                df = df.reindex(columns=columns)
            else:
                # Handle the case when 'fieldValue' column is missing
                df = pd.DataFrame([])

            json_data = {
                "headerInfo": header_info,
                "inputSet": paginated_data,
                "paginationInfo": pagination_info
            }

            pagination = paginated_data.to_dict(orient='records')
            # print('response display', response_display)
            response = {
                'data': pagination,
                'Page Num': page,
                'Page Size': per_page,
                'Total Pages': total_pages,
            }

            return render_template('search_pagination.html', response=response, all_keys=output_columns,
                                   input_set=input_set_data, search_param1=search_param1, search_param2=search_param2)


        else:
            # Return all data with pagination when no search parameters are provided
            # Pagination parameters
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))

            total_records = len(response_display)
            total_pages = (total_records + per_page - 1) // per_page

            # Calculate start and end index for pagination
            start_index = (page - 1) * per_page
            end_index = start_index + per_page

            print('response display outside search', response_display)
            # Apply pagination to inputSet
            input_set = []
            for row_index, row in response_display.iterrows():
                print('outside search row', row)
                print(f'outsdie search ,Start index:{start_index} End index:{end_index}  and row_index:{row_index}')

                if row_index >= start_index and row_index < end_index:
                    for col_index, value in enumerate(row):
                        print('outside search col and col value', col_index, value)
                        if response_display.columns[col_index] in matching_data:
                            print('outside search Inside if ', response_display.columns[col_index])
                            input_set.append({
                                "fieldName": matching_data[response_display.columns[col_index]],
                                "fieldDesc": response_display.columns[col_index],
                                "fieldValue": response_display.iloc[row_index, col_index],
                                'fieldIndex': row_index + 1
                            })

                    print(f"All values in Row {row_index} processed.")

            # Create pagination metadata
            pagination_info = {
                "page": page,
                "per_page": per_page,
                "total_records": total_records,
                "total_pages": total_pages
            }

            input_set_data = input_set
            input_set_df = pd.DataFrame(input_set)
            if 'fieldValue' in input_set_df.columns:
                df = pd.pivot_table(input_set_df, index='fieldIndex', columns='fieldDesc', values='fieldValue',
                                    aggfunc=lambda x: x)
                df = df.reset_index(drop=True)
                # df['Index_position'] = range(start_index + 1, end_index + 1)
                columns = [col for col in df.columns if col != 'Index_position']
                df = df.reindex(columns=columns)
            else:
                # Handle the case when 'fieldValue' column is missing
                df = pd.DataFrame([])

            json_data = {
                "headerInfo": header_info,
                "inputSet": df,
                "paginationInfo": pagination_info
            }

            pagination = df.to_dict(orient='records')
            response = {
                'data': pagination,
                'Page Num': page,
                'Page Size': per_page,
                'Total Pages': total_pages,
            }

            return render_template('pagination3.html', response=response, all_keys=df.columns, input_set=input_set_data)

    ### super working copy
    # @app.route("/API/1.0/DataGenResponseSet", methods=['GET'])
    # def data_gen_response_set():
    #
    #     matching_data = {
    #         "Entity": "PBUKR",
    #         "Start Date": "PLFEZ",
    #         "End Date": "PLSEZ",
    #         "Client": "ZZ_CLIENT",
    #         "Requester E-Mail": "Email",
    #         "Engagement Type": "PRART",
    #         "Eng Partner": "Z3",
    #         "Eng Manager": "Z4"
    #     }
    #
    #     search_param1 = request.args.get('DataSet_GUID')
    #     search_param2 = request.args.get('DataSet_Name')
    #
    #     display_object = Generated_data_display()
    #     response_display = display_object.Screen_Data_display(dat_frame, input_dict)
    #
    #     response_display.to_excel(r'sample_synthetic/output_file2.xlsx', index=False)
    #     response_display = pd.read_excel(r'sample_synthetic/output_file2.xlsx')
    #     response_display = response_display.applymap(lambda x: x.astype(int) if isinstance(x, np.int64) else x)
    #
    #     header_info = {
    #         "processAreaId": input_dict['ProcessAreaId'],
    #         "dataSetName": input_dict["DataSetName"],
    #         "TargetSys": input_dict["TargetSys"],
    #         "CountryKey": input_dict['CountryKey'],
    #         # "numOfRecords": input_dict['NumOfRecords']
    #     }
    #
    #     if search_param1 and search_param2:
    #         df = pd.read_excel(r'sample_synthetic/DB_Tables.xlsx', sheet_name='DataSet_ENG')
    #         response_display = df[(df['DataSet_GUID'] == search_param1) & (df['DataSet_Name'] == search_param2)]
    #
    #         # # Prepare the response
    #         ## response = {
    #         ##     'filtered_data': response_display.to_dict(orient='records')
    #         # }
    #     # Pagination parameters
    #     page = int(request.args.get('page', 1))
    #     per_page = int(request.args.get('per_page', 10))
    #     total_records = len(response_display)
    #     total_pages = (total_records + per_page - 1) // per_page
    #
    #     # Calculate start and end index for pagination
    #     start_index = (page - 1) * per_page
    #
    #     end_index = start_index + per_page
    #     print("start index", start_index, "end index", end_index)
    #
    #     # Apply pagination to inputSet
    #     input_set = []
    #     for row_index, row in response_display.iterrows():
    #         if row_index >= start_index and row_index < end_index:
    #             for col_index, value in enumerate(row):
    #                 if response_display.columns[col_index] in matching_data:
    #                     input_set.append({
    #                         "fieldName": matching_data[response_display.columns[col_index]],
    #                         "fieldDesc": response_display.columns[col_index],
    #                         "fieldValue": response_display.iloc[row_index, col_index],
    #                         'fieldIndex': row_index + 1
    #                     })
    #
    #             print(f"All values in Row {row_index} processed.")
    #
    #     # # Create pagination metadata
    #     pagination_info = {
    #         "page": page,
    #         "per_page": per_page,
    #         "total_records": total_records,
    #         "total_pages": total_pages
    #     }
    #
    #     print('Input data set ', input_set)
    #     input_set_data = input_set
    #     print("pagination_info data", pagination_info)
    #     input_set_df = pd.DataFrame(input_set)
    #     if 'fieldValue' in input_set_df.columns:
    #         df = pd.pivot_table(input_set_df, index='fieldIndex', columns='fieldDesc', values='fieldValue',
    #                             aggfunc=lambda x: x)
    #         df = df.reset_index(drop=True)
    #         df['Index_position'] = range(start_index + 1, end_index + 1)
    #         columns = ['Index_position'] + [col for col in df.columns if col != 'Index_position']
    #         df = df.reindex(columns=columns)
    #         print('latest data df', df)
    #     else:
    #         # Handle the case when 'fieldValue' column is missing
    #         df = pd.DataFrame([])
    #
    #
    #     json_data = {
    #         "headerInfo": header_info,
    #         "inputSet": df,
    #         "paginationInfo": pagination_info
    #     }
    #
    #     print('JSon data latest', json_data['inputSet'])
    #     pagination = df.to_dict(orient='records')
    #     response = {
    #         'data': pagination,
    #         #  'data':response,
    #         'Page Num': page,
    #         'Page Size': per_page,
    #         'Total Pages': total_pages,
    #
    #     }
    #
    #     return render_template('pagination3.html', response=response, all_keys=df.columns, input_set=input_set_data)



    @app.route("/API/1.0/DataGenRequestSet", methods=['POST'])
    def data_gen_request_set():
        data = request.get_json()
        header_info = data["HeaderInfo"]
        input_set = data["InputSet"]
        Action = request.args.get('Action')
        print('header info', header_info)

        header_dict2 = {"Process_Area": header_info['ProcessAreaId'], "DataSet_GUID":"", "DataSet_Name": header_info['DataSetName'],
                        "Created_On": header_info["Created_On"],"Created_By": header_info["Created_By"],
                        "Changed_On": header_info['Changed_On'], "Changed_By": header_info['Changed_By'], "Status": header_info["Status"], 'Stage':header_info['Stage'], 'DataSet_Table': "DTT"}
        #print(input_set)
        header_info['Action'] = Action
        bulk_object = Bulk_Driver()
        responselist = bulk_object.bulk_driver_method(header_info, input_set)
        print('Response LISt', responselist)

        header_obj = Header_DB_Class()
        db_obj = header_obj.save_header_to_dataset_sheet_db(header_dict2, header_info['NumOfRecords'])
        df_obj = header_obj.save_output_df_dataset_ENG_db()

        global dat_frame
        global input_dict

        dat_frame = responselist[0]
        input_dict = responselist[1]
        # print('gloabl input dictionary', input_dict)



        return "Data posted successfully! "


    @app.route("/API/1.0/display_paged_data", methods=['GET'])
    def display_paged_data():
        display_object = Generated_data_display()
        response_display = display_object.Screen_Data_display(dat_frame, input_dict)
        # print("second response")
        print("return printed_display_data", response_display)


        response_display.to_excel(r'sample_synthetic/output_file.xlsx', index=False)


        df = pd.read_excel(r'sample_synthetic/output_file.xlsx')
        page = int(request.args.get('page', 1))
        page_limit = int(request.args.get('page_limit', 10))

        start = (page - 1) * (page_limit)
        end = start + page_limit

        total_pages = (len(df) + page_limit - 1) // page_limit

        print('Total pages', total_pages)

        pagination = df.iloc[start:end].to_dict(orient='records')

        response = {
           'data': pagination,
           #  'data':response,
            'Page Num': page,
            'Page Size': page_limit,
            'Total Pages': total_pages,
            # 'Index':row_index
        }
        # return jsonify(response)

        all_keys = []
        for d in response['data']:
            for key in d.keys():
                if key not in all_keys:
                    all_keys.append(key)
                else:
                    continue

        print('all keys::', list(all_keys))
        return render_template(r'pagination.html', response=response, all_keys=all_keys)


    # @app.route('/API/1.0/search', methods=['GET'])
    # def search():
    #
    #     dataset_guid = request.args.get('DataSet_GUID')
    #     print('DS GUID', dataset_guid)
    #     dataset_name = request.args.get('DataSet_Name')
    #
    #     # Load the Excel file into a pandas DataFrame
    #     df = pd.read_excel(r'sample_synthetic/DB_Tables.xlsx',sheet_name='DataSet_ENG')
    #
    #     # Filter the DataFrame based on the provided criteria
    #     filtered_df = df[(df['DataSet_GUID'] == dataset_guid) & (df['DataSet_Name'] == dataset_name)]
    #
    #     # Prepare the response
    #     response = {
    #         'filtered_data': filtered_df.to_dict(orient='records')
    #     }
    #
    #     return jsonify(response)


    @app.route('/API/1.0/download_excel')
    def download_excel():
        excel_file_path = r'sample_synthetic/output_file.xlsx'
        return send_file(excel_file_path, as_attachment=True)


    @app.route('/API/1.0/display_data')
    def display_data():
        df = pd.read_excel(r'sample_synthetic/output_file.xlsx')
        rows = df.to_dict('records')

        # Get the column names
        columns = df.columns.tolist()

        return render_template(r'table.html', columns=columns, rows=rows)





    @app.route('/API/1.0/')
    def index():
        return render_template(r'index.html')

except Exception as e:
    print('Flask API call', e)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
