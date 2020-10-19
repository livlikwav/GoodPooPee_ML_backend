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

    * Warning : redis save data by byte type
    So encode before saving,
    And decode when get data.
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
            host='gpp-redis', port=6379, db=0
            
            Docker-compose make service names. And it resolve name to the correct container IP address
            I named redis container 'gpp-redis'. So, use it.
        '''
        self.rd = redis.Redis(host='gpp-redis', port=6379, db=0)

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
        self.rd.hset(ppcam_id, 'ppsnack', data.encode('UTF-8'))
        # check that successfully added on redis
        if(self.rd.hget(ppcam_id, 'ppsnack') is not None):
            return True
        else:
            raise Exception('Fail to get ppsnack state from redis')

    def save_pad(self, ppcam_id: int, data: str) -> bool:
        '''
            Persist pad (POST or PUT)
        '''
        self.rd.hset(ppcam_id, 'pad', data.encode('UTF-8'))
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

    def get_all(self, ppcam_id: int) -> dict:
        '''
            Return all state of ppcam
            1. ppsnack
            2. pad
            3. feeding
            :Return: dict (only)
        '''
        # init dict
        resp = {}
        # first, get all states
        ppsnack = self.get_ppsnack(ppcam_id)
        pad = self.get_pad(ppcam_id)
        feeding = self.get_feeding(ppcam_id)
        # check None for all states
        if(ppsnack is not None):
            resp['ppsnack'] = ppsnack
        if(pad is not None):
            resp['pad'] = pad
        if(feeding is not None):
            resp['feeding'] = feeding
        # clear all states of that ppcam_id
        self.rd.delete(ppcam_id)
        # return result dict
        return resp


    def get_ppsnack(self, ppcam_id: int) -> dict:
        '''
            Get ppsnack state of ppcam_id
            dict|None
        '''
        resp = self.rd.hget(ppcam_id, 'ppsnack')
        if(resp is not None):
            return json.loads(resp.decode('UTF-8')) # redis return byte type. so decode
        else:
            return None

    def get_pad(self, ppcam_id: int) -> dict:
        '''
            Get pad state of ppcam_id
            dict|None
        '''
        resp = self.rd.hget(ppcam_id, 'pad')
        if(resp is not None):
            return json.loads(resp.decode('UTF-8')) # redis return byte type. so decode
        else:
            return None

    def get_feeding(self, ppcam_id: int) -> int:
        '''
            Get feeding state of ppcam_id
            int|None
        '''
        resp = self.rd.hget(ppcam_id, 'feeding')
        if(resp is not None):
            return resp.decode() # redis return val is byte. so decode
        else:
            return None