#from cdispyutils.hmac4 import get_auth
import json
#import local_settings
import requests

import flask

app = flask.Flask(__name__)

#JSON GET endpoint
#@app.route('/json', methods=['GET'])
#def get-json-metadata():
#    data = query(query_txt, auth, api_url)
#    return data

@app.route('/json/<path:id>') # 'path' allows the use of '/' in the id
def get_json_metadata(id):
    metadata = get_metadata_dict(id)
    return translate_dict_to_json(metadata)

# translate a dictionary to a json string
def translate_dict_to_json(d):
    str = json.dumps(d)
    return str

# create a dictionary containing the metadata for a given object_id
def get_metadata_dict(object_id):
    response = query_metadata(object_id) # query to peregrine

    # translate the response to a dictionary
    data = response.get_json()['data']
    #file_type = next(iter(data.keys())) # name of first key = file type
    #metadata = data[file_type][0] # get metadata
    metadata = flatten_dict(data)
    #for key, value in metadata.items():
    #    print(key, value)
    return metadata

# flatten a dictionary, assuming there are no key duplicates
def flatten_dict(d):
    flat_d = {}
    for k, v in d.items():
        if isinstance(v, list):
            flat_d.update(flatten_dict(v[0]))
        else:
            flat_d.update({k:v})
    return flat_d

# write a query and transmits it to send_query()
def query_metadata(object_id):
    file_type = 'submitted_aligned_reads'
    query_txt = '{ ' + file_type + ' (object_id: "' + object_id + """") {
        core_metadata_collections {
          title
          description
          creator
          contributor
          coverage
          language
          publisher
          rights
          source
          subject
        }
        file_name
        data_format
        file_size
        object_id
        updated_datetime
      }
    }"""
    #print(query_txt)
    data = send_query(query_txt)
    return data

# send a query to peregrine and return the jsonified response
def send_query(query_txt):
    query = {'query': query_txt}

    api_url = app.config.get('API_URL')
    if not api_url:
        return flask.jsonify({'error': 'pidgin is not configured with API_URL'}), 500

    #print(flask.request.headers)
    auth = flask.request.headers.get('Authorization')

    output = requests.post(api_url, headers={'Authorization': auth}, json=query).text
    #print(output)

    output = """{
      "data": {
        "aligned_reads_index": [
          {
            "core_metadata_collections": [
              {
                "contributor": "DCP",
                "coverage": "US",
                "creator": "Pauline",
                "language": "en-US"
              }
            ],
            "data_format": "JPG",
            "file_name": "pauline_test.jpg"
          }
        ]
      }
    }"""

    data = json.loads(output)
    return flask.jsonify(data)
