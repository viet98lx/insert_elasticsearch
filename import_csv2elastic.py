import csv
from elasticsearch import Elasticsearch 
from elasticsearch.helpers import bulk

def csv2json(file):
    print('Running csv2json...')
    jsonArray = []
    #read csv file
    with open(file, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            jsonArray.append(row)
    print('Done')
    return jsonArray

def import_csv_elastic(jsonArr, es, index_name):
    print('Running import_elastic...')
    print('len arr import:',len(jsonArr))

    actions = [
        {
            "_index": index_name,
            "_source": item
        } for item in jsonArr
    ]
    bulk(es, actions)
    print('Done import')
    return

def import_json_elastic(jsonArr, es, index_name):
    actions = [
        {
            "_index": index_name,
            "_source": item
        } for item in jsonArr
    ]
    bulk(es, actions, doc_type='_doc')
    print('Done import')
    return

