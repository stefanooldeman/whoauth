from flask import json
from flask import Flask, request, Response, jsonify
import json
import pdb

application = Flask(__name__)
app = application

@app.route('/auth/access_token', methods=['GET', 'POST'])
def authorize_endpoint():
    # check request body
    required_entities = [u'grant_type', u'username', u'password']
    optional_entities = [u'scope']
    found = 0
    # in debug mode, duplicate the required_entities items and pop each when found
    missing_keys = [] 
    missing_keys.extend(required_entities)
    for key in request.form.keys():
        # we are whitelisting here, ignore all other params that were sent
        if key in required_entities:
            found += 1
            #in debug mode
            i = missing_keys.index(key)
            missing_keys.pop(i)

    if len(required_entities) != found:
        data = {'error': 'invalid_request'}
        # when debug, send the list of found params
        data['missing_entity'] = missing_keys
        resp = jsonify(data)
        resp.status_code = 400
        resp.headers['Cache-Control'] = 'no-store'
        resp.headers['Pragma']        = 'no-cache'
        return resp

    # validate credentials username and password


    # send payload

    data = {
            'access_token'      : '42374690y41yd0BXC.df-7629013eo',
            'token_type'        : 'example',
            'expires_in'        : '3600', #recommended
            'refresh_token'     : 'thSDTFy237f208IkAw021', #optional
            }

    resp= jsonify(data)
    resp.status_code= 200
    resp.headers['Content-type']  = 'application/json;charset=UTF-8'
    resp.headers['Cache-Control'] = 'no-store'
    resp.headers['Pragma']        = 'no-cache'
    return resp

