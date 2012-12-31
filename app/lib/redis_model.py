import redis

class RedisModel(object):

    TOMY2_SALT = '(*f01h3jedlnA*90du1pj-1.BHS)dhu_)0@-0312h_'

    # redis INCR Keys
    KEYS_USER_UID = 'global:nextUserId'

    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

