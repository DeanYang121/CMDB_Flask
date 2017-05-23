#encoding:utf-8

import pickle
import time

import redisHelper
from server.hosts import monitored_groups


def config_serializer(client_ip,detail=False):
    applied_services = []
    configs = {
        'services':{}
    }
    for group in monitored_groups:
        for monitor_ip in group.hosts:
            if monitor_ip == client_ip:
                applied_services.extend(group.services)

    applied_services = set(applied_services)

    if detail is True:
        return applied_services
    for service_class in applied_services:
        service_ins = service_class()
        _result = [service_ins.interval,service_ins.plugin_name,time.time()]
        configs['services'][service_ins.name] = _result
    return configs

# def all_host_configs():
#     configs = {'hosts':{}}
#     applied_services = []
#     for group in monitored_groups:
#         for host_ip in group.hosts:
#             configs['hosts'][host_ip] = {}
#     print(configs) # {'hosts': {'127.0.0.1': {}}}
#     return configs
#
# def get_host_configs(service_instance,msg):
#     ipaddr = msg.get('ip')
#     print('get here ...')
#     configs = config_serializer(ipaddr)
#     service_instance.redis.set(ipaddr,pickle.dumps(configs))
#     return True

#发送给单个客户端服务器需要的配置信息
def flush_all_host_config_into_redis():
    applied_host = []
    redis = redisHelper.redisHelper()
    for group in monitored_groups:
        applied_host.extend(group.hosts)
    applied_host = set(applied_host)
    for host_ip in applied_host:
        host_config = config_serializer(host_ip)
        print(host_config)
        key = 'hostconfig:%s'%host_ip
        redis.set(key,pickle.dumps(host_config))



if __name__=="__main__":
    flush_all_host_config_into_redis()
    # print(config_serializer('127.0.0.1'))
    #all_host_configs()
    print("end")