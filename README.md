# NGS_Demo (VCF parser)
Using Python 3.5.2
Application pulls a PDF file that simulates a client's manifest with the name of patient, date of birth and name of VCF file.
It iterates through the list and looks for the VCF files in the location given. It creates a JSON object with the demographic data points (patient name, date of birth and VCF File name) plus the data in the VCF File (converted to JSON format).
It sends a REST POST request to local mongodb instance.
The REST endpoints were created using Eve and the VCF file parser is written in accordance to
https://samtools.github.io/hts-specs/VCFv4.2.pdf

Information about the data and the application
VCF files were collected from NCBI, parsed and populated into a Mongo DB by the script
demo/demo.py. This Mongo DB was running in the docker image Mongo (https://hub.docker.com/_/mongo/).

Endpoints and methods:
GET http://0.0.0.0:5000/ngs_data - Returns all of the NGS_Data parsed found in DB.
POST http://0.0.0.0:5000/ngs_data/populate_db/<pdf_file_name> -
  - Must have a pdf file to parse in the /app folder
  - Populates the ngs_data file with the VCF files listed in the pdf file. See
    documentation in /app/pdf_demographics_parser.py
GET http://0.0.0.0:5000/ngs_data/<_id> - Return NGS Data from the item _id field. You can get this id
                                         by running GET http://0.0.0.0:5000/ngs_data
DELETE http://0.0.0.0:5000/ngs_data - Deletes all the data found in the ngs_data document.
DELETE http://0.0.0.0:5000/ngs_data/<_id> - Deletes NGS Data from the item _id field.

How to run the demo and API
Dependencies:
docker
docker-compose
git

Steps:
1) Run git clone https://github.com/sacktla/NGS_Demo.git
2) Move into the NGS_Demo folder.
3) Run docker-compose build
4) Run docker-compose up
5) Using Postman send a request GET http://0.0.0.0:5000/ngs_data.
   This will return the empty document for ngs_data .
6) Using Postman send a request POST http://0.0.0.0:5000/ngs_data/pupulate_db/test_demographics.pdf
   This will populate the ngs_data document.
7) Using Postman send a request GET http://0.0.0.0:5000/ngs_data. This will
   return the ngs_data document with all of the parsed and populated data.
