import pdftotext
import re
import datetime

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
        with open(file_name, 'rb') as pdf_file_stream:
            pdf = pdftotext.PDF(pdf_file_stream)
            for page in pdf:
                bones += page
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

        extract_date  = lambda a: re.search(\
                                '[0-9]{2}/[0-9]{2}/[0-9]{4}', a)
        extract_first = lambda a: re.match('[a-zA-Z]+', a)
        extract_last  = lambda a: re.search(' [a-zA-Z]+', a)
        extract_vcf   = lambda a: re.search('[a-zA-z._0-9]+.gz', a)

        for segment in test_corps.split('\n'):
            if header:
                header = False
                continue

            if segment != '':
                first_name    = extract_first(segment).group()
                last_name     = extract_last(segment).group().lstrip()
                vcf_file_name = extract_vcf(segment).group()
                birth_date    = extract_date(segment).group()

                temp_dem_dict = {
                                    'first_name':first_name,
                                    'last_name':last_name,
                                    'vcf_file_name':vcf_file_name,
                                    'birth_date':birth_date,
                                    'vcf_file_content':None,
                                }

                demographics.append(temp_dem_dict)

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
