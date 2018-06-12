#from cdispyutils.hmac4 import get_auth
import json
#import local_settings
import requests

from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return 'Flask says hello'

def query(query_txt, auth, api_url):
    print(query_txt)
    query = {'query': query_txt}
    output = requests.post(api_url, auth=auth, json=query).text
    data = json.loads(output)
    print(data)
    return data

#query_txt = '{core_metadata{id}}'
#query(query_txt, auth, api_url)

#def get_api_auth():
#  auth = get_auth(local_settings.ACCESS_KEY, local_settings.SECRET_KEY, 'submission')
#  return auth

#if __name__ == '__main__':
#    print('main')
#    args = parse_cmd_args()
#    auth = get_api_auth()

#JSON GET endpoint
#@app.route('/json', methods=['GET'])
#def get-json-metadata():
#    data = query(query_txt, auth, api_url)
#    return data
