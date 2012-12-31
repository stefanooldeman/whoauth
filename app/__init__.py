from flask import json
from flask import Flask, request, Response, jsonify
import redis
import simplejson as json
import hashlib
import pdb

from lib import utils

application = Flask(__name__)
app = application
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

TOMY2_SALT = '(*f01h3jedlnA*90du1pj-1.BHS)dhu_)0@-0312h_'

@app.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    data = redis.hgetall('user:%d' % uid)
    if(data == {}):
        abort(404)

    return jsonify(data), 200

# FIXME validate input 
# TODO protect against spam requests..
@app.route('/users', methods=['POST'])
def create_user():
    input_data = json.loads(request.data)
# TODO generate this.. and make the names cute / fun
    # FIXME ensure the names are unique
    generated_username = 'fdshjfsdu'
    # remember id value is a String type
    uid = redis.incr('ids:user')
    password_hash = hashlib.sha224(TOMY2_SALT + input_data['password']).hexdigest()
    data = {
            'uid': uid,
            'username': generated_username,
            'email': input_data['email']
            }
    # user namespace = user details
    redis.hmset('user:%s' % uid, data)
    # cred namespace = credentials schema
    redis.set('cred:%s:uid' % generated_username, uid)
    redis.set('cred:%s:hash' % uid, password_hash)

    return jsonify(data), 201

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
        return utils.response_with(data, 400)

    # check request body
    response = utils.validate_body([u'grant_type'], request.form.keys())
    if (response):
        return response 
    else:
        grant_type = request.form['grant_type']

    if (grant_type == 'password'):
        # Grant Flow: "Resource Owner Password Credentials Grant"

        response = validate_body([u'username', u'password'], request.form.keys())
        if (response):
            return response
        else:
#FIXME filter input
            username = request.form['username']
            password = request.form['password']

        # validate credentials username and password
        if (validate_credentials(username, password) is True):
# TODO generate a token and store it with user
            data = {
                    'access_token'      : '42374690y41yd0BXC.df-7629013eo',
                    'token_type'        : 'Bearer',
                    'expires_in'        : '3600'
                    }
            #in debug
            data['uid'] = get_uid_with(username) 
            return response_with(data, 200)
        else:
            data = {'error': 'invalid_grant'}
            # in debug
            data['error_description'] = 'invalid password credentials'
            return response_with(data, 400)
    else:

# TODO write some unit tests here
def validate_credentials(username, password):
    password_hash = hashlib.sha224(TOMY2_SALT + password).hexdigest()
    found_uid      = get_uid_with(username)
    if (found_uid != None):
        found_hash = redis.get('cred:%s:hash' % found_uid)
        if (found_hash != None and password_hash == found_hash):
            return True

    return False
        return utils.response_with({'error': 'unsupported_grant_type'}, 400)

def get_uid_with(username):
    return redis.get('cred:%s:uid' % username)


@app.errorhandler(404)
def not_allowed(error):
    data = {
            'error'             : 'invalid_request',
            'error_description' : 'Resource not found'
            }
    return utils.response_with(data, error.code)

@app.errorhandler(405)
def not_allowed(error):
    data = {
            'error'             : 'invalid_request',
            'error_description' : 'Method not allowed, use POST'
            }
    return utils.response_with(data, error.code)
