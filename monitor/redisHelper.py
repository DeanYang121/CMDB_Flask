#encoding:utf-8

import redis,time
import pickle

class redisHelper(object):
    def __init__(self):
        self.__conn=redis.Redis(host='192.168.196.145',port=6379)
        self.chan_sub = 'fm11.1'
        self.chan_pub = 'fm11.1'

    def get(self,key):
        return self.__conn.get(key)

    def set(self,key,value):
        self.__conn.set(key,value)

    def public(self,msg):
        self.__conn.publish(self.chan_pub,msg)

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.chan_sub)
        #pub.parse_response()
        while True:
            for msg in pub.listen():
                #print(pickle.loads(msg['data']))
                # print(msg)
                 if msg['type'] == 'message':
                     cat = msg['channel']
                     hat = pickle.loads(msg['data'])
                     return  ('订阅: %s 频道的信息 %s' % (cat, hat))


if __name__=="__main__":
    t = redisHelper()
    # while True:
    #     mess = t.subscribe()
    #     time.sleep(3)
    while True:
        t.subscribe()
        time.sleep(3)
