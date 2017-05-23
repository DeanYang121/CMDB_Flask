#encoding: utf-8
from server import linux


class BaseTemplate(object):
    def __init__(self):
        self.name = 'yourTemplateName'
        self.group_name='yourgroupname'
        self.hosts=[]
        self.services=[]

class LinuxTemplate(BaseTemplate):
     def __init__(self):
         super(LinuxTemplate, self).__init__()
         self.name='linuxTemplate'
         self.services=[
             linux.cpu,
             # linux.memory,
         ]

class NetworkTemplate(BaseTemplate):
    def __init__(self):
        super(NetworkTemplate, self).__init__()
        self.name = 'NetworkTemplate'
        self.services = [
            linux.network,
        ]



if __name__ == '__main__':
    t = LinuxTemplate()
    t.hosts = ['192.168.1.135']
    for service in t.services:
        service = service()
        print(service.name,service.interval,)