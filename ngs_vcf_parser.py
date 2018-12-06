import gzip
import json
import ntpath


class NGS_Parser(object):
    def __init__(self, file_name, decode_type='UTF-8'):
        self.content   = None
        self.file_name = file_name
        self.format    = {}
        self.info      = {}
        self.filter    = {}
        self.reference = None
        self.data      = []

        self.extract_vcf(file_name, decode_type)

    def to_json(self):
        return json.dumps(
            {
                ntpath.basename(self.file_name) : {
                    "format"    : self.format,
                    "info"      : self.info,
                    "filter"    : self.filter,
                    "reference" : self.reference,
                    "data"      : self.data
                }
            }
        )

    def extract_vcf(self, file_name, decode_type):
        with gzip.open(file_name) as gz_file:
            content = gz_file.read().splitlines()

            extracted_reference = ''
            extracted_format = {}
            header = False

            for i in range(len(content)):
                content[i] = content[i].decode(decode_type)

                if content[i].startswith("##INFO"):
                    self.extract_helper(content[i], doc_type="info")

                elif content[i].startswith("##reference"):
                    self.reference = content[i].split('=')[1]

                elif content[i].startswith("##FORMAT"):
                    self.extract_helper(content[i], doc_type="format")

                elif content[i].startswith("##FILTER"):
                    self.extract_helper(content[i], doc_type="filter")

                elif content[i].startswith('#')\
                 and not content[i].startswith('##'):
                    header  = True

                elif not content[i].startswith("#") and header:
                    self.extract_data(content[i])

            return content if len(content) > 0 else None

    def extract_helper(self, line, doc_type):
        if doc_type == "info":
            use_dict = self.info
        elif doc_type == "format":
            use_dict = self.format
        elif doc_type == "filter":
            use_dict = self.filter
        else:
            print("Doc Type {} has not been considered for parsing".format(doc_type))
            return

        key = None
        info_line = line.split("<")[1]
        info_line = info_line.replace('>', '')

        for param in info_line.split(','):
            param_list = param.split('=')
            param_name = param_list[0]

            if param_name == 'ID':
                key = param_list[1]
                use_dict[key] = {}

            if key:
                if param_name == "Number":
                    use_dict[key]["Number"] = param_list[1]
                elif param_name == "Type":
                    use_dict[key]["Type"] = param_list[1]
                elif param_name == "Description":
                    use_dict[key]["Description"] = param_list[1]

    #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
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
