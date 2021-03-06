# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
from import_csv2elastic import *
from elasticsearch import Elasticsearch
import argparse
import json

es=Elasticsearch([{'host':'localhost','port':9200}])
print(es)

if __name__ == '__main__':
    # file_path = '/home/viet/Downloads/shorten_filtered_ebds_30k_predict_v3.csv'
    parser = argparse.ArgumentParser(description='Argument parse for flask api.')
    parser.add_argument('--file', type=str, required=True, default='shorten_filtered_ebds_30k_predict.csv',
                        help='file need index')
    parser.add_argument('--index_name', type=str, required=True, default='index_example',
                        help='index name')
    parser.add_argument('--mapping_field_file', type=str, default=None)
    args = parser.parse_args()
    name = args.index_name
    mapping_file = args.mapping_field_file
    file_path = args.file
    if mapping_file is not None:
        mapping_obj = json.load(open(mapping_file))
        response = es.indices.create(
            index=name,
            body=mapping_obj,
            ignore=400  # ignore 400 already exists code
        )
        # print out the response:
        print('response:', response)
    if 'csv' in file_path:
        jsonArray = csv2json(file_path)
        import_csv_elastic(jsonArray, es, name)
    if 'json' in file_path:
        f = open(file_path)
        jsonArray = json.load(f)
        import_csv_elastic(jsonArray, es, name)
        f.close()
    # es.indices.delete(index='filtered_30k_intent_v3', ignore=[400, 404])
    # pass
