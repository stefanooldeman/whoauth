from app.lib.redis_model import RedisModel as BaseModel
import hashlib

class User(BaseModel):

    data = {}

    def __init__(self):
        super(User, self).__init__()
        # user namespace contains user details
        self.namespace = 'user'
        self.hash_keys = ['uid', 'username', 'email']

    # @id unique-user-id
    # @return Boolean
    def load(self, id):
        self.data = self.redis.hgetall('user:%d' % id)
        # when {} record is not found, returns False
        return self.data is not {}

    def create(self, input_data):
        username = self.generate_username()
        # remember id value is a String type
        password_hash = self.generate_password(input_data['password'])
        data = {
                'username': username,
                'email': input_data['email']
                }
        if (self.insert(data, True) is False):
            #add logging
            pass

        # cred namespace = credentials schema
        self.redis.set('cred:%s:uid' % username, self.uid)
        self.redis.set('cred:%s:hash' % self.uid, password_hash)
        self.data = data

        # TODO pipe all redis requests and return variable Bool on result
        return True

    def generate_password(self, data):
        return hashlib.sha224(self.TOMY2_SALT + data).hexdigest()

    def generate_username(self):
        # TODO generate this.. and make the names cute / fun
        # FIXME ensure the names are unique
        return "Fhuidf"

    # TODO write some unit tests here
    def validate_credentials(self, username, password):
        password_hash = generate_password(password)
        found_uid      = self.get_uid_with(username)
        if (found_uid != None):
            found_hash = self.redis.get('cred:%s:hash' % found_uid)
            if (found_hash != None and password_hash == found_hash):
                return True

        return False

    def get_uid_with(self, username):
        return self.redis.get('cred:%s:uid' % username)

    # Base class implementations #
    def get_next_uid(self):
        return self.redis.incr('globals:nextUserId')

