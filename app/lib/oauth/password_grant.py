import redis
import hashlib
from base import OAuth
from app.lib import utils

redis = redis.StrictRedis(host='localhost', port=6379, db=0)

class Flow(OAuth):

    def validate(self, data):
        # Grant Flow: "Resource Owner Password Credentials Grant"

        response = utils.validate_body([u'username', u'password'], data)
        if (response):
            return response
        else:
            #FIXME filter input
            username = data['username']
            password = data['password']

        # validate credentials username and password
        if (self.validate_credentials(username, password) is True):
            # TODO generate a token and store it with user
            data = {
                    'access_token'      : '42374690y41yd0BXC.df-7629013eo',
                    'token_type'        : 'Bearer',
                    'expires_in'        : '3600'
                    }
            #in debug
            data['uid'] = self.get_uid_with(username) 
            return utils.response_with(data, 200)
        else:
            data = {'error': 'invalid_grant'}
            # in debug
            data['error_description'] = 'invalid password credentials'
            return utils.response_with(data, 400)

    # TODO write some unit tests here
    def validate_credentials(self, username, password):
        TOMY2_SALT = '(*f01h3jedlnA*90du1pj-1.BHS)dhu_)0@-0312h_'
        password_hash = hashlib.sha224(TOMY2_SALT + password).hexdigest()
        found_uid      = self.get_uid_with(username)
        if (found_uid != None):
            found_hash = redis.get('cred:%s:hash' % found_uid)
            if (found_hash != None and password_hash == found_hash):
                return True

        return False

    def get_uid_with(self, username):
        return redis.get('cred:%s:uid' % username)

