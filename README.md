# NGS_Demo (VCF parser)
Using Python 3.5.2
Application pulls a PDF file that simulates a client's manifest with the name of patient, date of birth and name of VCF file.
It iterates through the list and looks for the VCF files in the location given. It creates a JSON object with the demographic
data points (patient name, date of birth and VCF File name) plus the data in the VCF File (converted to JSON format).
It sends a REST POST request to local mongodb instance.
The REST endpoints were created using Eve and the VCF file parser is written in accordance to
https://samtools.github.io/hts-specs/VCFv4.2.pdf

Instructions to run the demo

1) Create a virtual environment and make sure all the dependencies listed
   in the requirements.txt file are installed. Make sure you also have Mongo DB
   installed.
2) Activate the virtual environment.
3) Clone the NGS_Demo folder. Navigate to the folder.
4) Set up your FLASK_APP variable to app.py
    "export FLASK_APP=app.py"
5) In a separate instance, start your Mongo DB in your local computer at the default port (mongodb://          localhost:27017)
6) Go back to the session where you exported the FLASK_APP variable and type "flask run".
    This will start the REST API.
7) Go to a third session and run the script demo.py. This will grab the PDF file Test_Data/test_demographics.pdf file, parse it, find the vcf files in the Test_Data folder, parse them
and store them in the Mongo DB.
Make sure you update locations in demo.py to where the Test_Data folder is found.
8) Use postman to get all the parsed VCF files in a JSON format.
  http://0.0.0.0:5000/ngs_data/ You can access individual records by grabbing the fields
  of _items["_id"]. You can delete individual records or all of them.

Instructions using docker image:
1) Pull docker image from Docker Hub: sacktla/ngs_demo
  docker pull sacktla/ngs_demo:
2)
