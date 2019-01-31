# NGS_Demo (VCF parser)
Information about the data and the application:
- The REST endpoints were created using Eve and the VCF file parser is written in accordance to
  https://samtools.github.io/hts-specs/VCFv4.2.pdf
- VCF files were collected from NCBI.
- Mongo DB image is from https://hub.docker.com/_/mongo/

Endpoints and methods:

GET http://0.0.0.0:5000/ngs_data
  - Returns all of the ngs_data collection.

POST http://0.0.0.0:5000/ngs_data/populate_db/<pdf_file_name> -
  - The PDF file must exist in the /app folder
  - Iterates through the list of patients found in the PDF file
    identifies the first name, last name, DOB and VCF file name for each
    record. It searches for the VCF file in the /app/Test_Data folder.
    A JSON object is created with the demographic data points and the VCF
    data in a JSON format. The JSON object is stored in the Mongo DB for the
    ngs_data collection.

GET http://0.0.0.0:5000/ngs_data/<_id>
  - Returns the document identified by the _id field.

DELETE http://0.0.0.0:5000/ngs_data
  - Deletes the ngs_data collection.

DELETE http://0.0.0.0:5000/ngs_data/<_id>
  - Deletes document identified by the _id field.

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
   This will return the empty collection for ngs_data .
6) Using Postman send a request POST http://0.0.0.0:5000/ngs_data/pupulate_db/test_demographics.pdf
   This will populate the ngs_data collection.
7) Using Postman send a request GET http://0.0.0.0:5000/ngs_data. This will
   return the ngs_data collection with all of the parsed and populated data.
