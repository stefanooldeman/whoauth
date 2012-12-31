import password_grant as PasswordGrant

class OAuthFlow(object):

    @staticmethod
    def factory(grant_type):
        if (grant_type == 'password'):
            return PasswordGrant.Flow()
        raise NotImplementedError()
        

