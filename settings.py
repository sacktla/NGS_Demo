#Connection to Mongo
MONGO_URI = 'mongodb://localhost:27017/ngs-demo'

#Allow resources to have write endpoint
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

#Define a schema
ngs_data_schema = {
    'first_name':{'type':'string'},
    'last_name':{'type':'string'},
    'vcf_file_name':{'type':'string'},
    'birth_date':{'type':'string'},#NEED TO WORK ON GETTING THE DATA AS A DATE
    'vcf_file_content':{'type':'dict'},
}

DOMAIN = {
    'ngs_data':{
        'schema':ngs_data_schema,
    },
}
