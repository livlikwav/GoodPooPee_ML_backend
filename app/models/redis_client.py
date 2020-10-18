import redis

class RedisClient:
    '''
        RedisClient for state management between app and ppcam
    '''
    def __init__(self):
        '''
            host='localhost', port=6379, db=0
        '''
        self.rd = redis.Redis(host='localhost', port=6379, db=0)

    def size(self):
        '''
            check number of ppcams
            dbsize() return number of keys
        '''
        return self.rd.dbsize()