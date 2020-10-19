'''
    Redis for state management
    Persist to request of updating models.
    1. Pad
    2. Ppsnack
    3. Feeding

    Use Redis hashes
    Key: Ppcam_id
    Field: Model name (Pad or ppsnack)
    Value: JSON(data)
'''
import json
import logging
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
    
    def save_ppsnack(self, ppcam_id: int, data: str) -> bool:
        '''
            Persist ppsnack (POST or PUT)
        '''
        self.rd.hset(ppcam_id, 'ppsnack', data)
        # check that successfully added on redis
        if(self.rd.hget(ppcam_id, 'ppsnack') is not None):
            return True
        else:
            raise Exception('Fail to get ppsnack state from redis')

    def save_pad(self, ppcam_id: int, data: str) -> bool:
        '''
            Persist pad (POST or PUT)
        '''
        self.rd.hset(ppcam_id, 'pad', data)
        # check that successfully added on redis
        if(self.rd.hget(ppcam_id, 'pad') is not None):
            return True
        else:
            raise Exception('Fail to get pad state from redis')

    def save_feeding(self, ppcam_id: int) -> dict:
        '''
            Persist feeding command of app for ppsnack (POST)
            Return dict for count of feeding command
        '''
        self.rd.hincrby(ppcam_id, 'feeding') # default amount = 1
        # check that successfully added on redis
        feeding_count = self.rd.hget(ppcam_id, 'feeding').decode() # redis return val is byte. so decode
        if(feeding_count is not None):
            return {
                "feeding" : feeding_count,
            }
        else:
            raise Exception('Fail to get feeding state from redis')