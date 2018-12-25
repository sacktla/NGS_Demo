# NGS_Demo (VCF parser)
Application pulls a PDF file that simulates a client's manifest with the name of patient, date of birth and name of VCF file.
It iterates through the list and looks for the VCF files in the location given. It creates a JSON object with the demographic
data points (patient name, date of birth and VCF File name) plus the data in the VCF File (converted to JSON format). 
It sends a REST POST request to local mongodb instance. 
The REST endpoints were created using Eve and the VCF file parser is written in accordance to 
https://samtools.github.io/hts-specs/VCFv4.2.pdf
