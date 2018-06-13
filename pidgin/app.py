#from cdispyutils.hmac4 import get_auth
import json
#import local_settings
import requests

import flask

app = flask.Flask(__name__)

#@app.route('/')
#def root():
#    return 'Flask says hello'

#JSON GET endpoint
#@app.route('/json', methods=['GET'])
#def get-json-metadata():
#    data = query(query_txt, auth, api_url)
#    return data

@app.route('/json/<path:id>') # 'path' allows the use of '/' in the id
def get_json_metadata(id):
    data = get_metadata(id)
    return data

def get_metadata(id):
    #id = "dg.4503/1e4142b8-4266-49ae-a452-b64d5f803a4c"
    #query_txt = """{ submitted_aligned_reads {

    file_type = 'submitted_aligned_reads'

    query_txt = '{ ' + file_type + ' (object_id: "' + id + """") {
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
    print(query_txt)

    data = send_query(query_txt)
    print("Data:")
    print(data)

    return data

def send_query(query_txt):
    query = {'query': query_txt}

    api_url = app.config.get('API_URL')
    if not api_url:
        return flask.jsonify({'error': 'pidgin is not configured with API_URL'}), 500

    #print(flask.request.headers)
    auth = flask.request.headers.get('Authorization')

    output = requests.post(api_url, headers={'Authorization': auth}, json=query).text
    #print(output)
    data = json.loads(output)
    return flask.jsonify(data)

#def get_api_auth():
#  auth = get_auth(local_settings.ACCESS_KEY, local_settings.SECRET_KEY, 'submission')
#  return auth

#if __name__ == '__main__':
#    print('main')
#    args = parse_cmd_args()
#    auth = get_api_auth()
