import pdftotext
import re
import datetime

class PDF_Demographics_Parser(object):

    def __init__(self, file_name):
        self.text_corps   = PDF_Demographics_Parser.extract_text(file_name)
        self.file_name    = file_name
        self.demographics = PDF_Demographics_Parser.create_demographics(\
                                self.text_corps)

    @classmethod
    def extract_text(cls, file_name):
        bones = ''
        with open(file_name, 'rb') as pdf_file_stream:
            pdf = pdftotext.PDF(pdf_file_stream)
            for page in pdf:
                bones += page
        return bones

    @classmethod
    def create_demographics(cls, test_corps):
        header       = True
        demographics = []

        #Not the most ideal regular expressions but will do for the demo
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
                # birth_date    = datetime.datetime(int(date[2]),\
                                    # int(date[0]), int(date[1]))

                temp_dem_dict = {
                                    'first_name':first_name,
                                    'last_name':last_name,
                                    'vcf_file_name':vcf_file_name,
                                    'birth_date':birth_date,
                                    'vcf_file_content':None,
                                }

                demographics.append(temp_dem_dict)

        return demographics

    def to_json(self):
        return json.dumps(
            {
                ntpath.basename(self.file_name) : self.demographics
            }
        )
