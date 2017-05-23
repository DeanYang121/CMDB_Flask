#encoding:utf-8

from server.data_process import avg
from server.generic import BaseService


class network(BaseService):
    def __init__(self):
        super(network, self).__init__()
        self.name = 'nic_network'
        self.interval = 120
        self.plugin_name = 'get_network_info'
        self.triggers={
            'in':{'func':avg,
                  'minutes':15,
                  'operator':'gt',
                  'warning':80,
                  'critical':90,
                  'data_type':'percentage'
            }
        }