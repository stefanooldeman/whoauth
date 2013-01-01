from flask import jsonify
import utils

class Utils(object):

    # returns False if valid, otherwise an response object
    @staticmethod
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
            return Utils.response_with(data, 400)
        return False


    @staticmethod
    def response_with(data, status):
        resp = jsonify(data)
        resp.status_code = status
        resp.headers['Content-type']  = 'application/json;charset=UTF-8'
        resp.headers['Cache-Control'] = 'no-store'
        resp.headers['Pragma']        = 'no-cache'
        return resp
