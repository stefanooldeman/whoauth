from base import OAuth
from app.lib import utils
from app.model.user import User


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

        user = User()
        # validate credentials username and password
        if (user.validate_credentials(username, password) is True):
            # TODO generate a token and store it with user
            data = {
                    'access_token'      : '42374690y41yd0BXC.df-7629013eo',
                    'token_type'        : 'Bearer',
                    'expires_in'        : '3600'
                    }
            #in debug
            data['uid'] = user.get_uid_with(username) 
            return utils.response_with(data, 200)
        else:
            data = {'error': 'invalid_grant'}
            # in debug
            data['error_description'] = 'invalid password credentials'
            return utils.response_with(data, 400)

