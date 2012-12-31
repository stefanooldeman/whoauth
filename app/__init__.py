from flask import json
from flask import Flask, request, Response, jsonify, abort

from lib import utils
from lib.oauth import OAuthFlow
from app.model.user import User

application = Flask(__name__)
app = application

TOMY2_SALT = '(*f01h3jedlnA*90du1pj-1.BHS)dhu_)0@-0312h_'

@app.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    user = User()
    if(user.load(uid) == False):
        abort(404)
    return jsonify(user.data), 200

# FIXME validate input 
# TODO protect against spam requests..
@app.route('/users', methods=['POST'])
def create_user():
    input_data = json.loads(request.data)
    user = User()
    if (user.create(input_data) is False):
        abort(401)

    return jsonify(user.data), 201

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
