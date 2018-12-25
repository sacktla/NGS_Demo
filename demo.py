from ngs_vcf_parser import NGS_Parser
from pdf_demographics_parser import PDF_Demographics_Parser
from os import path
import json
import requests
"""
This script will just populate the ngs_data endpoint so that you can access
it via Postman. 
"""
#update TEST_DEMOGRAPHICS to point to the PDF file with the demographics and
#VCF file Name
TEST_DEMOGRAPHICS = '/Users/jesuszaragoza/Desktop/NGS_Parser/NGS_Demo/Test_Data/test_demographics.pdf'
#Update VCF_LOCATION to the Test_Data Folder location
VCF_LOCATION = '/Users/jesuszaragoza/Desktop/NGS_Parser/NGS_Demo/Test_Data'
def main():
    demographics = PDF_Demographics_Parser(TEST_DEMOGRAPHICS).demographics
    for demo in demographics:
        vcf_file_name            = demo['vcf_file_name']
        vcf_file_path            = path.join(VCF_LOCATION, vcf_file_name)
        vcf_file_content         = NGS_Parser(vcf_file_path)
        demo['vcf_file_content'] = vcf_file_content.to_dict()

    requests.post(url='http://127.0.0.1:5000/ngs_data/',\
                    data=json.dumps(demographics), headers={'Content-Type':'application/json'})

if __name__ == '__main__':
    main()
