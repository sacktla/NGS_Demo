from eve import Eve
from ngs_vcf_parser import NGS_Parser
from pdf_demographics_parser import PDF_Demographics_Parser
from os import path
import json
import requests
from flask import request
import os
import subprocess

VCF_LOCATION = os.path.join(os.getcwd(),'app/Test_Data')

app = Eve()

"""
Endpoint to populate database with parsed PDF file. The PDF file will be
parsed by pdftotext version 0.72.0. Endpoint will check whether PDF file exists
and that the method is POST.

See test_demographics.pdf for layout of PDF file.
The VCF files listed in the pdf file must be found in the Test_Data folder.

pdftotext version 0.72.0:
 -Copyright 2005-2018 The Poppler Developers - http://poppler.freedesktop.org
 -Copyright 1996-2011 Glyph & Cog, LLC
"""
@app.route('/ngs_data/populate_db/<pdf_file_name>', methods=['POST'])
def populate_db(pdf_file_name):
    if request.method == 'POST':

        pdf_file_path = os.path.join(os.getcwd(), 'app', pdf_file_name)

        if os.path.exists(pdf_file_path):
            output_file_path = os.path.join(os.getcwd(), 'app', \
                               pdf_file_name.replace('.pdf', '.txt'))

            subprocess.call(['/usr/bin/pdftotext', pdf_file_path, output_file_path])

            demographics = PDF_Demographics_Parser(output_file_path).demographics

            for demo in demographics:
                vcf_file_name            = demo['vcf_file_name']
                vcf_file_path            = path.join(VCF_LOCATION, vcf_file_name)
                vcf_file_content         = NGS_Parser(vcf_file_path)
                demo['vcf_file_content'] = vcf_file_content.to_dict()

            status = requests.post(url='http://0.0.0.0:5000/ngs_data',\
                            data=json.dumps(demographics), \
                            headers={'Content-Type':'application/json'}).status_code
            message = "Database populated status: {}".format(status)
        else:
            message = "PDF File does not exists in " + \
                        os.path.join(os.getcwd(), 'app')
            status = 404
    else:
        message = "Method must be POST"
        status = 405

    message = json.dumps({"message": message})
    print(status)
    return app.response_class(message, content_type="application/json", status=status)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
