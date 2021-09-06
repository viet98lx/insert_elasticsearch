import sys, time, io
import argparse
start_time = time.time()

if sys.version[0] != "3":
    print ("\nThis script requires Python 3")
    print ("Please run the script using the 'python3' command.\n")
    quit()

try:
    # import the Elasticsearch low-level client library
    from elasticsearch import Elasticsearch

    # import Pandas, JSON, and the NumPy library
    import pandas, json
    import numpy as np

except ImportError as error:
    print ("\nImportError:", error)
    print ("Please use 'pip3' to install the necessary packages.")
    quit()

# create a client instance of the library
print ("\ncreating client instance of Elasticsearch")
elastic_client = Elasticsearch([{'host':'localhost','port':9200}])

"""
MAKE API CALL TO CLUSTER AND CONVERT
THE RESPONSE OBJECT TO A LIST OF
ELASTICSEARCH DOCUMENTS
"""

if __name__ == '__main__':
    # file_path = '/home/viet/Downloads/shorten_filtered_ebds_30k_predict_v3.csv'
    parser = argparse.ArgumentParser(description='Argument parse for flask api.')
    parser.add_argument('--file', type=str, required=True, default='shorten_filtered_ebds_30k_predict.csv',
                        help='file need index')
    parser.add_argument('--index_name', type=str, required=True, default='index_example',
                        help='index name')
    parser.add_argument('--size', type=int, required=True, default='10000',
                        help='num docs')
    args = parser.parse_args()
    index_name = args.index_name
    file_path = args.file
    size = args.size

# total num of Elasticsearch documents to get with API call
# total_docs = 20
print ("\nmaking API call to Elasticsearch for", size, "documents.")
response = elastic_client.search(
    index=index_name,
    body={},
    size=size
)

# grab list of docs from nested dictionary response
print ("putting documents in a list")
elastic_docs = response["hits"]["hits"]

"""
GET ALL OF THE ELASTICSEARCH
INDEX'S FIELDS FROM _SOURCE
"""
#  create an empty Pandas DataFrame object for docs
docs = pandas.DataFrame()

# iterate each Elasticsearch doc in list
print ("\ncreating objects from Elasticsearch data.")
for num, doc in enumerate(elastic_docs):

    # get _source data dict from document
    source_data = doc["_source"]

    # get _id from document
    _id = doc["_id"]

    # create a Series object from doc dict object
    doc_data = pandas.Series(source_data, name = _id)

    # append the Series object to the DataFrame object
    docs = docs.append(doc_data)


"""
EXPORT THE ELASTICSEARCH DOCUMENTS PUT INTO
PANDAS OBJECTS
"""
print ("\nexporting Pandas objects to different file types.")

# export the Elasticsearch documents as a JSON file
docs.to_json(file_path+".json")

# have Pandas return a JSON string of the documents
# json_export = docs.to_json() # return JSON data
# print ("\nJSON data:", json_export)

# export Elasticsearch documents to a CSV file
docs.to_csv(file_path+".csv", ",") # CSV delimited by commas
print("export done")

# # export Elasticsearch documents to CSV
# csv_export = docs.to_csv(sep=",") # CSV delimited by commas
# print ("\nCSV data:", csv_export)