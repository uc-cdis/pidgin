import flask
import json
import requests

from pidgin.errors import *


app = flask.Flask(__name__)


@app.route('/<path:object_id>')
def get_core_metadata(object_id):
    """
    Get core metadata from an object_id.
    """
    accept = flask.request.headers.get('Accept')
    if accept == "x-bibtex":
        return get_bibtex_metadata(object_id)
    else: # accept == "application/json" or no accept header
        return get_json_metadata(object_id)


def get_json_metadata(object_id):
    """
    Get core metadata as JSON from an object_id.
    """
    try:
        metadata = get_metadata_dict(object_id)
        return json.dumps(metadata) # translate dictionary to json
    except PidginException as e:
        return e.message, e.code


def get_bibtex_metadata(object_id):
    """
    Get core metadata as BibTeX from an object_id.
    """
    metadata = get_metadata_dict(object_id)
    return translate_dict_to_bibtex(metadata)


def get_metadata_dict(object_id):
    """
    Create a dictionary containing the metadata for a given object_id.
    """
    response = request_metadata(object_id) # query to peregrine
    return flatten_dict(response) # translate the response to a dictionary


def translate_dict_to_bibtex(d):
    """
    Translate a dictionary to a BibTeX string.
    """
    items = ['{} = "{}"'.format(k, v) for k, v in d.items()]
    bibtex_items = ', '.join(items)
    bibtex_str = '@misc {' + d['object_id'] + ', ' + bibtex_items + '}'
    return bibtex_str


def flatten_dict(d):
    """
    Flatten a dictionary that contains core metadata.
    """
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
    except (AttributeError, IndexError):
        error = 'Core metadata not available for this file'
        if 'errors' in d:
            error += ': ' + d['errors'][0]
        raise NoCoreMetadataException(error)
    return flat_d


def get_file_type(object_id):
    """
    Get the type of file from the object_id.
    """
    query_txt = '{ datanode (object_id: "' + object_id + '") { type } }'
    response = send_query(query_txt)
    try:
        file_type = response['data']['datanode'][0]['type']
    except IndexError:
        raise ObjectNotFoundException('object_id "' + object_id + '" not found')
    return file_type


def request_metadata(object_id):
    """
    Write a query and transmit it to send_query().
    """
    file_type = get_file_type(object_id)

    # get the metadata from the type of file and the object_id
    query_txt = '''{{ {} (object_id: "{}") {{
        core_metadata_collections {{
            title description creator contributor coverage
            language publisher rights source subject
        }}
        type file_name data_format file_size
        project_id object_id updated_datetime }} }}
        '''.format(file_type, object_id)
    return send_query(query_txt)


def send_query(query_txt):
    """
    Send a query to peregrine and return the jsonified response.
    """
    api_url = app.config.get('API_URL')
    if not api_url:
        raise PidginException('Pidgin is not configured with API_URL')

    auth = flask.request.headers.get('Authorization')
    query = {'query': query_txt}
    response = requests.post(api_url, headers={'Authorization': auth}, json=query)
    data = response.json()

    if response.status_code == 403:
        raise AuthenticationException(data['message'])

    return data


@app.route('/_status', methods=['GET'])
def health_check():
    return 'Healthy', 200
