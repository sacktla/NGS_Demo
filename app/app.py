from eve import Eve
from ngs_vcf_parser import NGS_Parser
from pdf_demographics_parser import PDF_Demographics_Parser
from os import path
import json
import requests
from flask import request
import os

app = Eve()
TEST_DEMOGRAPHICS = os.path.join(os.getcwd(), 'app/test_demographics.txt')
#Update VCF_LOCATION to the Test_Data Folder location
VCF_LOCATION = os.path.join(os.getcwd(),'app/Test_Data')

@app.route('/ngs_data/populate_db', methods=['POST'])
def populate_db():
    if request.method == 'POST':
        demographics = PDF_Demographics_Parser(TEST_DEMOGRAPHICS).demographics
        for demo in demographics:
            vcf_file_name            = demo['vcf_file_name']
            vcf_file_path            = path.join(VCF_LOCATION, vcf_file_name)
            vcf_file_content         = NGS_Parser(vcf_file_path)
            demo['vcf_file_content'] = vcf_file_content.to_dict()


        status = requests.post(url='http://0.0.0.0:5000/ngs_data',\
                        data=json.dumps(demographics), headers={'Content-Type':'application/json'})
        message = json.dumps({"message": "Database populated"})
        return app.response_class(message, content_type='application/json', status=201)

    message = json.dumps({"message": "Method must be POST"})
    return app.response_class(message, content_type="application/json", status=405)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
