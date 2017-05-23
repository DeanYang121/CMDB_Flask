#encoding: utf-8
import gevent
from gevent import monkey;
from redisHelper import redisHelper
from server import serialize

monkey.patch_all()

class MonitorServer(object):
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.redis = redisHelper()

    def send_monitor_items(self):
        serialize.flush_all_host_config_into_redis()

    @staticmethod
    def recive_msg(self):
        msg = self.redis.subscribe()
        print('111111',msg)

    def handle(self):
        while True:
            gevent.joinall([
                gevent.spawn(MonitorServer.recive_msg(self)),
            ])


    def run(self):
        print('---starting monitor server----')
        self.handle()

    def process(self):
        pass
if __name__=="__main__":
    s = MonitorServer('0.0.0.0','8000')
    s.run()

