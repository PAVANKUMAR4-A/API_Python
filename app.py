import json
import requests

import pandas as pd
from flask import Flask, request,render_template,send_file,jsonify
from SDV_BULK_API_FILE.Header_DB import Header_DB_Class
import json
#from SDV_BULK_FILE.SDV_BULK_Driver_file import Bulk_Driver
from SDV_BULK_API_FILE.SDV_BULK_UPDATED_file_API import Bulk_Driver
from SDV_BULK_API_FILE.SDV_BULK_GET_Data_Display import Generated_data_display

app = Flask(__name__,template_folder='templates')

input_dict= {}
dat_frame = pd.DataFrame([])

try:
    @app.route("/API/1.0/DataGenRequestSet", methods=['POST','GET'])
    def data_gen_request_set():
        # df = pd.read_excel(r'file_paths/Conca_df.xlsx')

        data = request.get_json()
        header_info = data["HeaderInfo"]
        input_set = data["InputSet"]
        print('header info', header_info)

        header_dict2 = {"Process_Area": header_info['ProcessAreaId'], "DataSet_GUID":"", "DataSet_Name": header_info['DataSetName'],
                        "Created_On": header_info["Created_On"],"Created_By": header_info["Created_By"],
                        "Changed_On": header_info['Changed_On'], "Changed_By": header_info['Changed_By'], "Status": header_info["Status"], 'Stage':header_info['Stage'], 'DataSet_Table': "DTT"}
        #print(input_set)
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

        # dataset_guid = request.args.get('DataSet_GUID')
        # print('dataset_guid', dataset_guid)
        # dataset_name = request.args.get('DataSet_Name')
        #
        # # Load the Excel file into a pandas DataFrame

        #
        # # Filter the DataFrame based on the provided criteria
        # filtered_df = df[(df['DataSet_GUID'] == dataset_guid) & (df['DataSet_Name'] == dataset_name)]
        #
        # print('filtered df data ', filtered_df)
        # # Prepare the response
        # response = {
        #     'filtered_data': filtered_df.to_dict(orient='records')
        # }
        #
        # # return jsonify(response)
        #
        # # rows = response_display.to_json(orient='records')
        # # return rows

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
            'Total Pages': total_pages
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


    @app.route('/API/1.0/search', methods=['GET'])
    def search():

        dataset_guid = request.args.get('DataSet_GUID')
        print('DS GUID', dataset_guid)
        dataset_name = request.args.get('DataSet_Name')

        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(r'sample_synthetic/DB_Tables.xlsx',sheet_name='DataSet_ENG')

        # Filter the DataFrame based on the provided criteria
        filtered_df = df[(df['DataSet_GUID'] == dataset_guid) & (df['DataSet_Name'] == dataset_name)]

        # Prepare the response
        response = {
            'filtered_data': filtered_df.to_dict(orient='records')
        }

        return jsonify(response)


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