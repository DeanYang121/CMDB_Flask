#encoding: utf-8

class BaseService(object):
    def __init__(self):
        self.name = 'BaseService'
        self.interval = 300
        self.last_time = 0
        self.plugin_name = 'your_plugin_name' #插件名称
        self.triggers = {}  #阈值


