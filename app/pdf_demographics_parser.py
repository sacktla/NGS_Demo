# import pdftotext
import re
import datetime
import json
import ntpath
"""
Class used to extract data from PDF files simulating a manifest from a client
See Test_Data/test_demographics.pdf for example.
# NOTE: This is for demo only, not useful for production as it is very specific
to pdf file created for the purposes of this demo.
"""
class PDF_Demographics_Parser(object):

    """
    Initializer
    """
    def __init__(self, file_name):
        self.text_corps   = PDF_Demographics_Parser.extract_text(file_name)
        self.file_name    = file_name
        self.demographics = PDF_Demographics_Parser.create_demographics(\
                                self.text_corps)

    """
    Class method that extracts the text from a pdf file and returns
    it as a string.
    """
    @classmethod
    def extract_text(cls, file_name):
        bones = ''
        with open(file_name) as reader:
            bones = reader.read()
        return bones

    """
    Class method to obtain date, first and last name and name of vcf file
    Very specific to this demo. Regular expressions can be updated to make
    it more robust if metadata provided.
    """
    @classmethod
    def create_demographics(cls, test_corps):
        header       = True
        demographics = []

        content = []
        for segment in test_corps.splitlines():
            if segment != '':
                content.append(segment)

        idx = 0
        while idx < len(content):
            if idx != 0 and idx != 1 and idx != 2:
                if idx % 3 == 0:
                    first_name = content[idx].split()[0]
                    last_name = content[idx].split()[1]
                    idx += 1
                    vcf_file_name = content[idx]
                    idx += 1
                    birth_date = content[idx]

                temp_dem_dict = {
                                    'first_name':first_name,
                                    'last_name':last_name,
                                    'vcf_file_name':vcf_file_name,
                                    'birth_date':birth_date,
                                    'vcf_file_content':None,
                                }

                demographics.append(temp_dem_dict)
            idx += 1

        return demographics

    """
    Method that returns extracted data as a JSON file
    """
    def to_json(self):
        return json.dumps(
            {
                ntpath.basename(self.file_name) : self.demographics
            }
        )
