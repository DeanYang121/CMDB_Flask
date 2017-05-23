#encoding: utf-8
import pickle
import threading
import time


import plugin
from redisHelper import redisHelper

host_ip = '127.0.0.1'

class MonitorClient(object):
    def __init__(self,server,port):
        self.server = server
        self.port = port
        self.configs = {}
        self.redis = redisHelper()

    def format_msg(self,key,value):
        msg = {key: value}
        return pickle.dumps(msg)

    def get_config(self):
        config = self.redis.get('hostconfig:%s'%host_ip)
        if config:
            self.configs = pickle.loads(config)
            #print(self.configs) #{'services': {'linux_cpu': [30, 'get_cpu_info', 0]}}
            return True

    def handle(self):
            while True:
                if self.get_config():
                    print('----going to monitor service --- ', self.configs)
                    for service_name,val in self.configs['services'].items():
                        interval,plugin_name,loacl_time = val
                        print(interval,plugin_name)
                        t = threading.Thread(target=self.task,args=[service_name,plugin_name])
                        t.start()
                        self.configs['services'][service_name][2]=time.time()
                        print(self.configs)
                        time.sleep(15)
                else:
                    print('--could not found any configurations for this host---')

    def task(self,service_name,plugin_name):
        print('----going to run service',service_name,plugin_name)
        func = getattr(plugin, plugin_name)
        print(func)
        resulte = func()
        self.redis.public(pickle.dumps(resulte))

    def run(self):
        self.handle()

if __name__=="__main__":
    cli = MonitorClient('119.29.153.178','6379')
    cli.run()

