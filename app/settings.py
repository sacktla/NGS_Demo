#Connection to Mongo
MONGO_HOST="mongo"
MONGO_PORT=27017
MONGO_DBNAME = 'ngs_data'
#Allow resources to have write endpoint
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

#Define a schema
ngs_data_schema = {
    'first_name':{'type':'string'},
    'last_name':{'type':'string'},
    'vcf_file_name':{'type':'string'},
    'birth_date':{'type':'string'},
    'vcf_file_content':{'type':'dict'},
}

DOMAIN = {
    'ngs_data':{
        'schema':ngs_data_schema,
    },
}
