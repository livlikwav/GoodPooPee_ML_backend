'''
    Redis for state management
    Persist to request of updating models.
    1. Pad
    2. Ppsnack

    Use Redis hashes
    Key: Ppcam_id
    Field: Model name (Pad or ppsnack)
    Value: JSON(data)
'''
import redis

class RedisClient:
    '''
        RedisClient for state management between app and ppcam
    '''
    def __init__(self):
        '''
            host='host.docker.internal', port=6379, db=0
        '''
        self.rd = redis.Redis(host='host.docker.internal', port=6379, db=0)

    def size(self):
        '''
            check number of ppcams
            dbsize() return number of keys
        '''
        return self.rd.dbsize()