from flask import json
from flask import Flask, request, Response, jsonify
import json
import pdb

application = Flask(__name__)
app = application

# request method must be other than GET
# see ietf oauth v2 bearer (draft 22): section 2.2 Form-Encoded Body Parameter
# The HTTP request method is one for which the request body has defined semantics. In particular, this means that the GET method MUST NOT be used.
@app.route('/auth/access_token', methods=['POST'])
def access_token():

    required_header = 'application/x-www-form-urlencoded'
    if (request.headers['content-type'] != required_header):
        data = {'error': 'invalid_request'}
        # in debug mode
        data['error_description'] = 'missing header: ' + required_header
        return response_with(data, 400)

    # check request body
    response = validate_body([u'grant_type'], request.form.keys())
    if (response):
        return response 

    if (request.form['grant_type'] == 'password'):
        # Grant Flow: "Resource Owner Password Credentials Grant"

        response = validate_body([u'username', u'password'], request.form.keys())
        if (response):
            return response

        # TODO validate credentials username and password

        #send payload
        data = {
                'access_token'      : '42374690y41yd0BXC.df-7629013eo',
                'token_type'        : 'Bearer',
                'expires_in'        : '3600', #recommended
                'refresh_token'     : 'thSDTFy237f208IkAw021', #optional
                }
        return response_with(data, 200)
    else:
        return response_with({'error': 'unsupported_grant_type'}, 400)

# return False if valid, otherwise an response object
def validate_body(required_entities, keys):
    found = 0
    # in debug mode, duplicate the required_entities items and pop each when found
    missing_keys = [] 
    missing_keys.extend(required_entities)
    for key in keys:
        # we are whitelisting here, ignore all other params that were sent
        if key in required_entities:
            found += 1
            #in debug mode
            i = missing_keys.index(key)
            missing_keys.pop(i)

    if (len(required_entities) != found):
        data = {'error': 'invalid_request'}
        # when debug, send the list of found params
        # TODO, ensure error_description MUST NOT include chars outside the set %x20-21 / %x23-5B / %x5D-7E.
        data['error_description'] = 'missing_entity: %s' % str(missing_keys)
        return response_with(data, 400)
    return False

def response_with(data, status):
    resp = jsonify(data)
    resp.status_code = status
    resp.headers['Content-type']  = 'application/json;charset=UTF-8'
    resp.headers['Cache-Control'] = 'no-store'
    resp.headers['Pragma']        = 'no-cache'
    return resp

@app.errorhandler(405)
def not_allowed(error):
    data = {
            'error'             : 'invalid_request',
            'error_description' : 'Method not allowed, use POST'
            }
    return response_with(data, error.code)
