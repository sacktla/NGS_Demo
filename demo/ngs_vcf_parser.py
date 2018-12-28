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
        self.data        = []
        self.format      = []
        self.info        = []
        self.filter      = []
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
                    ntpath.basename(self.file_name).replace('.','_') :
                    {
                        "reference"   : self.reference,
                        "assembly"    : self.assembly,
                        "pedigree_DB" : self.pedigree_DB,
                        "file_format" : self.file_format,
                        "file_date"   : self.file_date,
                        "source"      : self.source,
                        "phasing"     : self.phasing,
                        "format"      : self.format,
                        "info"        : self.info,
                        "filter"      : self.filter,
                        "alt"         : self.alt,
                        "contig"      : self.contig,
                        "sample"      : self.sample,
                        "pedigree"    : self.pedigree,
                        "data"        : self.data,
                    }
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
                    self.extract_helper(content[i].replace("##INFO=", ""), doc_type="info")

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

                elif content[i].startswith("##FORMAT"):
                    self.extract_helper(content[i].replace("##FORMAT=", ""), doc_type="format")

                elif content[i].startswith("##FILTER"):
                    self.extract_helper(content[i].replace("##FILTER=", ""), doc_type="filter")

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
                "#CHROM"):
                    self.extract_data(content[i])

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
        info_dict  = {}

        for pair in info:
            split_pair     = pair.split('=')
            key            = split_pair[0]
            if len(split_pair) < 2:
                value = ''
            else:
                value = split_pair[1]

            info_dict[key] = value

        self.data.append(
            {
                'chromosome':chromosome,
                'position':position,
                'id':id,
                'reference':reference,
                'alternate':alternate,
                'quality':quality,
                'filter':filter,
                'info': info_dict,
            }
        )

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
