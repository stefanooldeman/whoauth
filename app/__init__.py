from flask import json
from flask import Flask, request, Response, jsonify, abort
import redis
import pdb
from lib import utils
from lib.oauth import OAuthFlow

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
    
    grant_type = request.form['grant_type']
    if (grant_type not in ['password']):
        return utils.response_with({'error': 'unsupported_grant_type'}, 400)

    grant = OAuthFlow.factory(grant_type)
    return grant.validate(request.form)


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
