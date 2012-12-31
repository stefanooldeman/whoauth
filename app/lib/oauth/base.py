class OAuth(object):
    def validate(self, data):
        raise NotImplementedError()
    def response(self):
        raise NotImplementedError()

