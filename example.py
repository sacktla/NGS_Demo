import gzip
import json
import ntpath

"""
Class to convert VCF files into JSON file.
"""
class NGS_Parser(object):

    """
    Initializer
    """
    def __init__(self, file_name, decode_type='UTF-8'):
        self.file_name   = file_name
        self.reference   = None
        self.assembly    = None
        self.pedigree_DB = None
        self.file_format = None
        self.file_date   = None
        self.source      = None
        self.phasing     = None
        self.filtered_data = {}
        self.non_filtered_data = {}
        self.info        = {}
        self.filter      = {}
        self.alt         = []
        self.contig      = []
        self.sample      = []
        self.pedigree    = []

        self.extract_vcf(file_name, decode_type)

    """
    Returns extracted data as a JSON object.
    """
    def to_json(self):
        return json.dumps(
            self.to_dict()
        )

    """
    Returns extracted data as a dictionary
    """
    def to_dict(self):
        return {
                    "reference"   : self.reference,
                    "assembly"    : self.assembly,
                    "pedigree_DB" : self.pedigree_DB,
                    "file_format"       : self.file_format,
                    "file_date"         : self.file_date,
                    "source"            : self.source,
                    "phasing"           : self.phasing,
                    "alt"               : self.alt,
                    "contig"            : self.contig,
                    "sample"            : self.sample,
                    "pedigree"          : self.pedigree,
                    "info"              : self.info,
                    "filtered_data"     : self.filtered_data,
                    "non_filtered_data" : self.non_filtered_data,
                }

    """
    Method to initiate extraction of VCF file
    """
    def extract_vcf(self, file_name, decode_type):
        with gzip.open(file_name) as gz_file:
            content = gz_file.read().splitlines()

            for i in range(len(content)):
                content[i] = content[i].decode(decode_type)

                if content[i].startswith("##INFO"):
                    self.parse_info(content[i])

                elif content[i].startswith("##reference"):
                    self.reference = content[i].split('=')[1]

                elif content[i].startswith("##fileformat"):
                    self.file_format = content[i].split('=')[1]

                elif content[i].startswith("##fileDate"):
                    self.file_date = content[i].split('=')[1]

                elif content[i].startswith("##source"):
                    self.source = content[i].split('=')[1]

                elif content[i].startswith("##phasing"):
                    self.phasing = content[i].split('=')[1]

                elif content[i].startswith("##FILTER"):
                    self.parse_filter(content[i])

                elif content[i].startswith("##ALT"):
                    self.extract_helper(content[i].replace("##ALT=", ""), doc_type="alt")

                elif content[i].startswith("##assembly"):
                    self.assembly = content[i].split('=')[1]

                elif content[i].startswith("##contig"):
                    self.extract_helper(content[i].replace("##contig=", ""), doc_type="contig")

                elif content[i].startswith("##SAMPLE"):
                    self.extract_helper(content[i].replace("##SAMPLE=", ""), doc_type="sample")

                elif content[i].startswith("##PEDIGREE"):
                    self.extract_helper(content[i].replace("##PEDIGREE=", ""), doc_type="pedigree")

                elif content[i].startswith("##pedigreeDB"):
                    self.pedigree_DB = content[i].split("=")[1].replace('<','')\
                        .replace('>','')

                elif not content[i].startswith(\
                "#CHROM") and not content[i].startswith("##FORMAT"):
                    self.extract_data(content[i])

    """
    Method to extract info field
    """
    def parse_info(self, line_content):

        clean_content = line_content.replace('##INFO=<', '')
        clean_content = clean_content.replace('>', '')
        split_content = NGS_Parser.separate_parameters(clean_content)
        info_key      = None
        idx           = 0

        while not info_key and idx < len(split_content):
            key, value = split_content[idx].split("=")

            if key == "ID":
                info_key = value

            idx += 1

        if info_key:
            self.info[info_key] = {}

            for field in split_content:
                key, value = field.split('=')
                self.info[info_key][key] = value

    """
    Method to extract filter field
    """
    def parse_filter(self, line_content):
        clean_content = line_content.replace("##FILTER=","")
        clean_content = clean_content.replace(">", "")
        split_content = NGS_Parser.separate_parameters(clean_content)
        filter_key    = None
        idx           = 0

        while not filter_key and idx < len(split_content):
            key, value = split_content[idx].split('=')

            if key == 'ID':
                filter_key = value

            idx += 1

        if filter_key:
            self.filter[filter_key] = {}

            for field in split_content:
                key, value = field.split('=')
                self.filter[info_key][key] = value

    """
    Method to extract information of VCF file.
    """
    def extract_helper(self, line, doc_type):
        if doc_type == "info":
            use_list = self.info
        elif doc_type == "format":
            use_list = self.format
        elif doc_type == "filter":
            use_list = self.filter
        elif doc_type == "alt":
            use_list = self.alt
        elif doc_type == "contig":
            use_list = self.contig
        elif doc_type == "sample":
            use_list = self.sample
        elif doc_type == "pedigree":
            use_list = self.pedigree

        info_line      = line.replace('<','')
        info_line      = info_line.replace('>', '')
        temp_info_dict = {}

        for param in NGS_Parser.separate_parameters(info_line):
            split_param                = param.split('=')
            param_name                 = split_param[0]
            param_value                = split_param[1].replace('"', '')
            temp_info_dict[param_name] = param_value

        use_list.append(temp_info_dict)

    """
    Method to extract data based on headers:
    CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
    """
    def extract_data(self, line):
        split_line = line.split('\t')
        chromosome = split_line[0]
        position   = split_line[1]
        id         = split_line[2]
        reference  = split_line[3]
        alternate  = split_line[4]
        quality    = split_line[5]
        filter     = split_line[6]
        info       = split_line[7].split(';')
        info_dict  = []

        for pair in info:
            split_pair = pair.split('=')
            key        = split_pair[0]

            data_type = self.info[key]['Type']
            # is_a_number = True
            # number = self.info[key]['Number']

            # try:
            #     _ = int(number)
            # except:
            #     is_a_number = False

            if data_type == "Flag":
                info_dict.append(
                    {
                        "key" : key,
                        # "description" : \
                        #         self.info[key]['Description'].replace('"', ""),
                        "values" : None,
                    }
                )
            else:
                info_dict.append(
                    {
                        "key" : key,
                        # "description" : \
                        #         self.info[key]['Description'].replace('"', ""),
                        "values" : split_pair[1],
                    }
                )
            # elif data_type != "String" or data_type != "Character":
            #     value = split_pair[1]
            #     info_dict.append(
            #         {
            #             "description" : \
            #                     self.info[key]['Description'].replace('"', ""),
            #             "values" : value,#.split(',') if not is_a_number or\
            #                             #int(number) > 1 else value,
            #
            #         }
            #     )
            #
            #     if not is_a_number or int(number) > 1:
            #         for idx in \
            #                 range(len(info_dict[len(info_dict) - 1]['values'])):
            #             if data_type == "Integer":
            #                 info_dict[len(info_dict) - 1]['values'][idx] =\
            #                 int(info_dict[len(info_dict) - 1]['values'][idx])
            #             elif data_type == "Float":
            #                 info_dict[len(info_dict) - 1]['values'][idx] = \
            #                 float(info_dict[len(info_dict) - 1]['values'][idx])
            #     else:
            #         if data_type == "Integer":
            #             info_dict[len(info_dict) - 1]['values'] = \
            #             int(info_dict[len(info_dict) - 1]['values'])
            #         elif data_type == "Float":
            #             info_dict[len(info_dict) - 1]['values'] = \
            #             float(info_dict[len(info_dict) - 1]['values'])

        if filter == "PASS":
            if id == '.':
                if not 'unknown' in self.non_filtered_data:
                    self.non_filtered_data['unknown'] = []

                self.non_filtered_data['unknown'].append(
                    {
                        'chromosome' : chromosome,
                        'position' : position,
                        'reference': reference,
                        'alternate' : alternate,
                        'quality' : quality,
                        'info' : info_dict,
                    }
                )
            else:
                self.non_filtered_data[id] = {
                    'chromosome' : chromosome,
                    'position' : position,
                    'reference': reference,
                    'alternate' : alternate,
                    'quality' : quality,
                    'info' : info_dict,
                }
        else:
            if id == '.':

                if not 'unknown' in self.non_filtered_data:
                    self.non_filtered_data['unknown'] = []

                self.filtered_data['unknown'].append(
                    {
                        'chromosome' : chromosome,
                        'position' : position,
                        'reference' : reference,
                        'alternate' : alternate,
                        'quality' : quality,
                        'info' : info_dict,
                        'filter' : [self.filter[id]['Description'] for id in \
                                                            filter.split(';')]
                    }
                )
            else:
                self.filtered_data[id] = {
                    'chromosome' : chromosome,
                    'position' : position,
                    'reference' : reference,
                    'alternate' : alternate,
                    'quality' : quality,
                    'info' : info_dict,
                    'filter' : [self.filter[id]['Description'] for id in \
                                                        filter.split(';')]
                }

    """
    Class Method to separate the information parameters to key=value elements
    separated by a comma. It allows us to escape the commas inside quotations
    Python csv package does not allow you to do this if the character "="
    is found.
    """
    @classmethod
    def separate_parameters(cls, string):
        new_list = []
        for i, b in enumerate(string.split(',')) :
            if b.find('=') != -1 :
                new_list.append(b)
            else :
                new_list[len(new_list)-1] += ',' + b

        return new_list
