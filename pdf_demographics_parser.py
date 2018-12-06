import pdftotext

class PDF_Demographics_Parser(object):

    def __init__(self, file_name):
        self.text_corps = PDF_Parser.extract_text(file_name)

    @classmethod
    def extract_text(cls, file_name):
        bones = ''
        with open(file_name, 'rb') as pdf_file_stream:
            pdf = pdftotext.PDF(pdf_file_stream)
            for page in pdf:
                bones += page
        return bones


pdf_parser = PDF_Parser('test_shit.pdf')
