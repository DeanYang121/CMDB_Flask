#encoding:utf-8
from server import template

g1 = template.LinuxTemplate()
g1.group_name = 'test groups'
g1.hosts = ['192.168.196.136']


g2= template.LinuxTemplate()
g2.group_name = 'pupet server group'
g2.hosts=['127.0.0.1','192.168.196.136']

monitored_groups = [g2]

if __name__=='__main__':
    print(g1.services[1]().name)