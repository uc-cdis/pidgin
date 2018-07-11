import json

import flask
import requests

from cdislogging import get_logger
# from pympler import tracker
import tracemalloc

app = flask.Flask(__name__)
app.snapshot = tracemalloc.take_snapshot()
app.logger = get_logger('pidgin')


# Endpoint to get core metadata as JSON from an object_id.
@app.route('/json/<path:object_id>') # 'path' allows the use of '/' in the id
def get_json_metadata(object_id):
    # tr = tracker.SummaryTracker()
    metadata = get_metadata_dict(object_id)
    a =translate_dict_to_json(metadata)
    # tr.print_diff()

    check_snapshot()

    return a


def check_snapshot():
    snapshot_2 = tracemalloc.take_snapshot()
    res =(snapshot_2.compare_to(flask.current_app.snapshot, 'lineno'))
    largest = res[0]
    if largest.size > 10000000:
        for entry in res[:5]:
            flask.current_app.logger.info(entry)


# Endpoint to get core metadata as BibTeX from an object_id.
@app.route('/bibtex/<path:object_id>') # 'path' allows the use of '/' in the id
def get_bibtex_metadata(object_id):
    metadata = get_metadata_dict(object_id)
    return translate_dict_to_bibtex(metadata)


# Create a dictionary containing the metadata for a given object_id.
def get_metadata_dict(object_id):
    response = request_metadata(object_id) # query to peregrine
    data = response.get_json()
    return flatten_dict(data) # translate the response to a dictionary


# Translate a dictionary to a JSON string.
def translate_dict_to_json(d):
    json_str = json.dumps(d)
    return json_str


# Translate a dictionary to a BibTeX string.
def translate_dict_to_bibtex(d):
    bibtex_str = '@misc {' + d['object_id'] + ', '
    for k, v in d.items(): # add each pair to the BibTeX output
        bibtex_str += k + ' = "' + str(v) + '", '
    bibtex_str += '}'
    return bibtex_str


# Flatten a dictionary, assuming there are no duplicates in the keys.
# (recursive)
def flatten_dict(d):
    def helper(d):
        flat_d = {}
        for k, v in d.items():
            if isinstance(v, list):
                if v: # check if there is data to read
                    # object_id is unique so the list should only contain one item
                    flat_d.update(helper(v[0]))
            elif isinstance(v, dict):
                if v: # check if there is data to read
                    flat_d.update(helper(v))
            else:
                flat_d.update({k:v})
        return flat_d
    result = helper(d)
    return result


# Flatten a dictionary, assuming there are no duplicates in the keys.
# (iterative)
def flatten_dict_iter(d):
    flat_d = {}
    try:
        data_type = list(d['data'].keys())[0]
        for k, v in d['data'][data_type][0].items():
            if k == 'core_metadata_collections':
                # object_id is unique so the list should only contain one item
                for k, v in v[0].items():
                    flat_d[k] = v
            else:
                flat_d[k] = v
    except Exception as e:
        error = 'Core metadata not available for this file'
        if d['errors']:
            error += ': ' + d['errors'][0]
        raise Exception(error)
    return flat_d


# Get the type of file from the object_id.
def get_file_type(object_id):
    query_txt = '{ datanode (object_id: "' + object_id + '") { type } }'
    response = send_query(query_txt)
    try:
        file_type = response.get_json()['data']['datanode'][0]['type']
    except IndexError:
        raise Exception("object_id not found")
    return file_type


# Write a query and transmit it to send_query().
def request_metadata(object_id):

    # get the metadata from the type of file and the object_id
    file_type = get_file_type(object_id)
    query_txt = '{ ' + file_type + ' (object_id: "' + object_id + """") {
        core_metadata_collections {
            title description creator contributor coverage
            language publisher rights source subject
        }
        file_name data_type data_format file_size object_id updated_datetime }
    }"""
    return send_query(query_txt)


# Send a query to peregrine and return the jsonified response.
def send_query(query_txt):
    # print(query_txt)
    query = {'query': query_txt}

    api_url = app.config.get('API_URL')
    if not api_url:
        raise Exception("Error: pidgin is not configured with API_URL")
        # return flask.jsonify({'error': 'pidgin is not configured with API_URL'}), 500

    auth = flask.request.headers.get('Authorization')

    output = requests.post(api_url, headers={'Authorization': auth}, json=query).text

    data = json.loads(output)
    return flask.jsonify(data)

# Health check endpoint.
@app.route('/_status', methods=['GET'])
def health_check():
    check_snapshot()
    return 'Healthy', 200
