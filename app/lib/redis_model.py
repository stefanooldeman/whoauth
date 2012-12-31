import redis

class RedisModel(object):

    TOMY2_SALT = '(*f01h3jedlnA*90du1pj-1.BHS)dhu_)0@-0312h_'

    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def insert(self, data, add_uid=False):
        #TODO add notice log when data does not contain all keys that are set in `hash_keys`
        uid = self.get_next_uid()
        if (add_uid):
            data['uid'] = uid
        self.uid = uid
        return self.update(uid, data)

    def update(self, uid, data):
         # remember id value is a String type
        key = "{1}:{0}".format(uid, self.get_namespace())
        return self.redis.hmset(key, data)

    def delete(self, uid):
        # remember id value is a String type
        key = "{1}:{0}".format(uid, self.get_namespace())
        args = get_hash_keys()
        return self.redis.hdel(key, *args)

    def get_hash_keys(self):
        if (self.hash_keys and isinstance(self.hash_keys, list)):
            raise NotImplementedError()

    def get_namespace(self):
        if (self.namespace is None):
            raise NotImplementedError()

    def get_next_uid(self):
        raise NotImplementedError()

