import json

import flask
import requests


app = flask.Flask(__name__)


# Endpoint to get core metadata as JSON from an object_id.
@app.route('/json/<path:object_id>') # 'path' allows the use of '/' in the id
def get_json_metadata(object_id):
    metadata = get_metadata_dict(object_id)
    return translate_dict_to_json(metadata)


# Endpoint to get core metadata as BibTeX from an object_id.
@app.route('/bibtex/<path:object_id>') # 'path' allows the use of '/' in the id
def get_bibtex_metadata(object_id):
    metadata = get_metadata_dict(object_id)
    return translate_dict_to_bibtex(metadata)


# Create a dictionary containing the metadata for a given object_id.
def get_metadata_dict(object_id):
    response = request_metadata(object_id) # query to peregrine
    data = response.get_json()
    metadata = flatten_dict(data) # translate the response to a dictionary
    return metadata


# Translate a dictionary to a JSON string.
def translate_dict_to_json(d):
    json_str = json.dumps(d)
    return json_str


# Translate a dictionary to a BibTeX string.
def translate_dict_to_bibtex(d):
    bibtex_str = '@misc {' + d['object_id'] + ',\n'
    for k, v in d.items(): # add each pair to the BibTeX output
        bibtex_str += k + ' = "' + str(v) + '",\n'
    bibtex_str += '}'
    return bibtex_str


# Flatten a dictionary, assuming there are no duplicates in the keys.
def flatten_dict(d):
    flat_d = {}
    for k, v in d.items():
        if isinstance(v, list):
            if v: # check if there is data to read
                # object_id is unique so the list should only contain one item
                flat_d.update(flatten_dict(v[0]))
        elif isinstance(v, dict):
            if v: # check if there is data to read
                flat_d.update(flatten_dict(v))
        else:
            flat_d.update({k:v})
    return flat_d


# Return a list of the values stored in a dict and its nested dict.
def get_nested_dict_values(d):
    values = []
    for k, v in d.items():
        if isinstance(v, list):
            for e in v:
                values.extend(get_nested_dict_values(e))
        elif isinstance(v, dict):
            values.extend(get_nested_dict_values(v))
        else:
            values.append(v)
    return values


# Get the type of file from the object_id.
def get_file_type(object_id):
    #TODO use this instead if object_id is added to node
    #query_txt = '{ node(object_id: "' + object_id + ') { node { type } }'
    #file_type = send_query(query_txt)
    # reformat output

    # get the list of available types from the graphql schema
    query_txt = '{ __schema { types { name } } }'
    all_file_types = send_query(query_txt)
    all_file_types = get_nested_dict_values(all_file_types.get_json())

    # for each type, check if it contains the file with this object_id
    for t in all_file_types:
        query_txt = '{ ' + t + ' (object_id: "' + object_id + '")' + ' { id } }'
        response = send_query(query_txt)
        response = response.get_json()
        if response['data'] and response['data'][t]:
            return t

    return flask.jsonify({'error': 'this object_id does not exist'}), 500


# Write a query and transmit it to send_query().
def request_metadata(object_id):
    file_type = get_file_type(object_id)

    # get the metadata from the type of file and the object_id
    query_txt = '{ ' + file_type + ' (object_id: "' + object_id + """") {
        core_metadata_collections {
            title description creator contributor coverage
            language publisher rights source subject
        }
        file_name data_format file_size object_id updated_datetime }
    }"""
    data = send_query(query_txt)
    return data


# Send a query to peregrine and return the jsonified response.
def send_query(query_txt):
    print(query_txt)
    query = {'query': query_txt}

    api_url = app.config.get('API_URL')
    if not api_url:
        return flask.jsonify({'error': 'pidgin is not configured with API_URL'}), 500

    auth = flask.request.headers.get('Authorization')

    output = requests.post(api_url, headers={'Authorization': auth}, json=query).text

    data = json.loads(output)
    return flask.jsonify(data)
