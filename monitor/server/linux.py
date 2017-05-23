#encoding: utf-8
from server import generic
from server.data_process import avg,hit


class cpu(generic.BaseService):
    def __init__(self):
        super(cpu,self).__init__()
        self.name = "linux_cpu"
        self.interval = 64
        self.plugin_name = "get_cpu_info"
        self.triggers={
            'idle':{'func':avg,
                    'minutes':15,
                    'operator':'lt',
                    'warning':20,
                    'critical':5,
                    'data_type':'percentage'
            },
            'iowait':{'func':hit,
                    'minutes':10,
                    'operator':'gt',
                    'threadhold':3,
                    'warning':50,
                    'critical':90,
                    'data_type':'int'
            },
        }

class memory(generic.BaseService):
    def __init__(self):
        super(memory, self).__init__()
        self.name='linux_memory'
        self.interval=60
        self.plugin_name='get_memory_info'
        self.triggers={
            'usage':{'func':avg,
                     'minutes':15,
                     'operaor':'gt',
                     'warning':80,
                     'critical':90,
                     'data_type':'percentage'
            }
        }

class network(generic.BaseService):
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

if __name__=="__main__":
    c = cpu()
    print(c.name,c.interval,c.plugin_name)

