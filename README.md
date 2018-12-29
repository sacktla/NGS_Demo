# NGS_Demo (VCF parser)
Using Python 3.5.2
Application pulls a PDF file that simulates a client's manifest with the name of patient, date of birth and name of VCF file.
It iterates through the list and looks for the VCF files in the location given. It creates a JSON object with the demographic
data points (patient name, date of birth and VCF File name) plus the data in the VCF File (converted to JSON format).
It sends a REST POST request to local mongodb instance.
The REST endpoints were created using Eve and the VCF file parser is written in accordance to
https://samtools.github.io/hts-specs/VCFv4.2.pdf

Information about the data and the application
VCF files were collected from NCBI, parsed and populated into a Mongo DB by the script
demo/demo.py. This Mongo DB was running in the docker image Mongo (https://hub.docker.com/_/mongo/).
After being populated with data, a copy of the Mongo image, with NGS data, was created
and published at https://cloud.docker.com/repository/docker/sacktla/mongo_ngs. This new image was
linked to the Docker container for this application https://cloud.docker.com/repository/docker/sacktla/ngs_demo_updated.

Instructions to run the API
1) Make sure you have docker and docker-compose installed in your computer.
2) Run the image
    docker run -p 5000:5000 sacktla/ngs_demo_updated
