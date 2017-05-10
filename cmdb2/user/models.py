from dbutils import MysqlConnection

import time
import ssh

class User(object):

    def __init__(self,id,username,password,age):
        self.id = id
        self.username = username
        self.password = password
        self.age = age

    @classmethod
    def get_list(cls,wheres=[]):
        _columns = ('id', 'username', 'password', 'age')
        _sql = 'select * from user where 1=1'
        _agrs = []
        for _key,_value in wheres:
            _sql += ' and {key} = %s'.format(key=_key)
            _agrs.append(_value)
        print(_sql)
        _cnt,_rt_lists = MysqlConnection.execute_sql(_sql,_agrs)
        _rt = []
        """与reboot的差别需要注意   注意如果返回的是空列表"""
        # return [dict(zip(_columns,_line)) for _line in _rt_lists]
        for _line in _rt_lists:
            _rt.append(dict(zip(_columns,_line)))

        return _rt

    @classmethod
    def get_by_name(cls,username):
        _rt = cls.get_list([('username',username)])
        return _rt[0] if len(_rt) > 0 else None

    @classmethod
    def get_by_id(cls,id):
        _rt = cls.get_list([('id',id)])
        return _rt[0] if len(_rt) >0 else None


    @classmethod
    def validate_login(self,username,password):
        _cnt = None
        _rt_list = []
        _column =('id','username')
        _sql = 'select id,username from user where username=%s and password=md5(%s)'
        _args = (username,password)
        _cnt,_rt_list = MysqlConnection.execute_sql(_sql,_args)

        return dict(zip(_column,_rt_list[0])) if _cnt != 0 else None

    @classmethod
    def validate_change_password(cls,user_id,manager_pwd,manager_name,user_pwd):

        if not cls.validate_login(manager_name,manager_pwd):
            return False,u'管理员密码错误'
        if cls.get_by_id(user_id) is None:
            return False,u'用户不存在'
        if len(user_pwd) < 6:
            return False,u'密码必须大于6位数'

        return True,''

    @classmethod
    def change_password(cls,user_id,user_pwd):
        _sql = "update user set password=md5(%s) where id = %s"
        _args = (user_pwd,user_id)
        MysqlConnection.execute_sql(_sql,_args,False)

    @classmethod
    def validate_change_info(cls,id,username,age):
        if cls.get_by_id(id) is None:
            return False,u'用户不存在'
        if not str(age).isdigit() or int(age)<=0 or int(age)>100 :
            return False,u'年龄必须是0到100的整数'
        return True,''

    @classmethod
    def change_info(cls,id,age):
        _sql = 'update user set age = %s where id = %s'
        _args = (age,id)
        MysqlConnection.execute_sql(_sql,_args,False)

    @classmethod
    def validate_add_user(cls,username,password,age):
        if username.strip() == '':
            return False,u'用户名不能为空'
        if cls.get_by_name(username):
            return False,u'用户已经存在'
        if len(password)<6 :
            return False,u'密码长度必须大于6位'
        if not str(age).isdigit() or int(age)<=0 or int(age)>100:
            return False,u'年龄必须是0到100的整数'

        return True,''

    @classmethod
    def add_user(cls,username,password,age):
        _sql = 'insert into user(username,password,age) value(%s,%s,%s)'
        _args = (username,password,age)
        MysqlConnection.execute_sql(_sql,_args,False)

    @classmethod
    def delete(cls,id):
        _sql = 'delete from user where id = %s'
        _args = (id,)
        MysqlConnection.execute_sql(_sql,_args,False)

class IDC(object):

    @classmethod
    def get_list(cls):
        return [(1, '北京-亦庄'), (2, '北京-酒仙桥'), (3, '北京-西单'), (4, '北京-东单')]

    @classmethod
    def get_list_dict(cls):
        return dict(cls.get_list())

class Asset(object):
    def __init__(self,sn, ip, hostname, os,
                        cpu, ram, disk,
                        idc_id, admin, business,
                        purchase_date, warranty, vendor, model, id=None, status=0):
        self.sn=sn
        self.ip=ip
        self.ip = ip
        self.hostname = hostname
        self.os = os
        self.cpu = cpu
        self.ram = ram
        self.disk = disk
        self.idc_id = idc_id
        self.admin = admin
        self.business = business
        self.purchase_date = purchase_date
        self.warranty = warranty
        self.vendor = vendor
        self.model = model
        self.status = status

    @classmethod
    def create_object(cls,obj):
        obj['purchase_date']=obj['purchase_date'].strftime('%Y-%m-%d')
        return obj

    @classmethod
    def get_by_key(cls,value,key='id'):
        _column = 'id,sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
        _columns = _column.split(',')
        _sql = 'select {column} from assets where status=0 and {key}=%s'.format(column=_column,key=key)
        _args = (value,)
        _count,_rt_lists = MysqlConnection.execute_sql(_sql,_args)

        return None if _count == 0 else cls.create_object(dict(zip(_columns,_rt_lists[0])))

    @classmethod
    def get_list(cls):
        _column = 'id,sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
        _columns = _column.split(',')
        '''实现方法二'''
        _rt=[]
        _sql='select {column} from assets where status=0'.format(column=_column)
        _count,_rt_lists=MysqlConnection.execute_sql(_sql)
        for _line in _rt_lists:
            _rt.append(cls.create_object(dict(zip(_columns,_line))))
        return _rt
        '''实现方法一'''
        # _sql = "select * from assets where 1=1 "
        # _args=[]
        # _rt = []
        # for _key,_value in wheres:
        #     _sql += ' and {key} = %s'.format(key=_key)
        #     _args.append(_value)
        # _cnt,_rt_lists=MysqlConnection.execute_sql(_sql,_args)
        # for _line in _rt_lists:
        #     _rt.append(dict(zip(_columns,_line)))
        # return _rt

    # @classmethod
    # def get_asset_list(cls):
    #     _column = 'id,sn,ip,hostname,os,cpu,ram,disk,idc_id,admin,business,purchase_date,warranty,vendor,model'
    #     _columns = _column.split(',')
    #     _sql = 'select {column} from assets where status = 0'.format(column=_columns)
    #     _count,_rt_lists = MysqlConnection.execute_sql(_sql)
    #     return [cls.create_object(dict(zip(_columns,_rt_list)) for _rt_list in _rt_lists)]

    @classmethod
    def validate_add(cls,req):
        _is_ok = True
        _errors = {}

        # print(req.get('hostname').strip())
        for _key in 'sn,ip,hostname,os,admin,business,vendor,model'.split(','):
            _value = req.get(_key,'').strip()
            if _value=='':
                _is_ok=False
                _errors[_key]='%s输入的值不能为空'%_key
            else:
                  if len(_value) >64 :
                      _is_ok=False
                      _errors[_key]='%s输入的字符不能超过64位'%_key

        if cls.get_by_key(req.get('sn'),'sn'):
            _is_ok = False
            _errors[_key] = 'sn 已经存在'
            print(_errors)

        if req.get('idc_id') not in [ str(_value[0]) for _value in IDC.get_list()] :
            _is_ok = False
            _errors['idc'] = '机房选择不正确！'

        _rules = {
            'cpu' : {'min' : 2, 'max' : 64},
            'ram' : {'min' : 2, 'max' : 512},
            'disk' : {'min' : 2, 'max' : 2048},
            'warranty' : {'min' : 1, 'max' : 5},
        }
        print(req.get('disk','3333333'))
        for _key in 'cpu,ram,disk,warranty'.split(','):
            _value = req.get(_key,'')
            if not _value.isdigit():
                _is_ok=False
                _errors[_key]='%s必须为数字'%_key
            else:
                _value = int(_value)
                _min = _rules.get(_key).get('min')
                _max = _rules.get(_key).get('max')
                if _value < _min or _value > _max:
                    _is_ok = False
                    _errors[_key] = '%s的取值范围为%s~%s'%(_key,_min,_max)

        if not req.get('purchase_date',''):
            _is_ok = False
            _errors['purchase_date'] = '采购日期不能为空！'

        return _is_ok,_errors

    @classmethod
    def add(cls,req):
        _column_str = 'sn,ip,hostname,os,admin,business,vendor,model,idc_id,cpu,ram,disk,warranty,purchase_date'
        _columns = _column_str.split(',')
        _args=[]
        for _arg in _columns:
            _args.append(req.get(_arg,''))

        _sql = 'INSERT INTO assets({columns}) VALUES({values})'.format(columns=_column_str, values=','.join(['%s'] * len(_columns)))
        MysqlConnection.execute_sql(_sql,_args,False)

    @classmethod
    def validate_update(cls,req):
        _is_ok = True
        _errors = {}

        # print(req.get('hostname').strip())
        for _key in 'sn,ip,hostname,os,admin,business,vendor,model'.split(','):
            _value = req.get(_key,'').strip()
            if _value=='':
                _is_ok=False
                _errors[_key]='%s输入的值不能为空'%_key
            else:
                  if len(_value) >64 :
                      _is_ok=False
                      _errors[_key]='%s输入的字符不能超过64位'%_key

        if req.get('idc_id') not in [ str(_value[0]) for _value in IDC.get_list()] :
            _is_ok = False
            _errors['idc'] = '机房选择不正确！'

        _rules = {
            'cpu' : {'min' : 2, 'max' : 64},
            'ram' : {'min' : 2, 'max' : 512},
            'disk' : {'min' : 2, 'max' : 2048},
            'warranty' : {'min' : 1, 'max' : 5},
        }
        print(req.get('disk','3333333'))
        for _key in 'cpu,ram,disk,warranty'.split(','):
            _value = req.get(_key,'')
            if not _value.isdigit():
                _is_ok=False
                _errors[_key]='%s必须为数字'%_key
            else:
                _value = int(_value)
                _min = _rules.get(_key).get('min')
                _max = _rules.get(_key).get('max')
                if _value < _min or _value > _max:
                    _is_ok = False
                    _errors[_key] = '%s的取值范围为%s~%s'%(_key,_min,_max)

        if not req.get('purchase_date',''):
            _is_ok = False
            _errors['purchase_date'] = '采购日期不能为空！'

        return _is_ok,_errors

    @classmethod
    def update_asset(cls,req):
        _column_str = 'sn,ip,hostname,os,admin,business,vendor,model,idc_id,cpu,ram,disk,warranty,purchase_date'
        _columns = _column_str.split(',')
        _values = []
        _args = []
        for _column in _columns:
            _values.append('{column}=%s'.format(column=_column))
            _args.append(req.get(_column, ''))

        _args.append(req.get('id'))

        _sql = 'UPDATE assets SET {values} WHERE id=%s'.format(values=','.join(_values))
        MysqlConnection.execute_sql(_sql, _args, False)

    @classmethod
    def delete(cls,id):
        _sql = 'delete from assets where id=%s'
        _args = (id,)
        MysqlConnection.execute_sql(_sql,_args,False)


class Command(object):

    @classmethod
    def validate(cls, req):

        admin_pwd = req.get('admin-password','')
        if admin_pwd !='123456':
            return False,u'管理员密码错误'

        return True, {}

    @classmethod
    def execute(cls,req):
        _id = req.get('id', '')
        _username = req.get('username', '')
        _password = req.get('password', '')
        _cmds = req.get('cmds', '').splitlines()
        _asset = Asset.get_by_key(_id)
        _result = ssh.ssh_execute(_asset['ip'], _username, _password, _cmds)
        _echos = []
        for _cmd, _outs, _errs in _result:
            _echos.append(_cmd)
            _echos.append(''.join(_outs))

        return '\n'.join(_echos)

class Performs(object):

    @classmethod
    def add(cls, req):
        _ip = req.get('ip')
        _cpu = req.get('cpu')
        _ram = req.get('ram')
        _time = req.get('time')
        _sql = 'insert into performs(ip, cpu, ram, time)values(%s, %s, %s, %s)';
        MysqlConnection.execute_sql(_sql, (_ip, _cpu, _ram, _time), False)

    @classmethod
    def get_list(cls, ip):
        _sql = 'SELECT cpu, ram, time FROM performs WHERE ip=%s and time>=%s order by time asc'
        # _sql = 'SELECT cpu, ram, time FROM performs WHERE ip=%s  order by time asc'
        # _args = (ip, )
        #表示60×60  表示一个小时之前的。三天前 60×60×24×3
        _args = (ip, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 60 * 60)))
        _count, _rt_list = MysqlConnection.execute_sql(_sql, _args)
        datetime_list = []
        cpu_list = []
        ram_list = []
        for _cpu, _ram, _time in _rt_list:
            cpu_list.append(_cpu)
            ram_list.append(_ram)
            datetime_list.append(_time.strftime('%H:%M:%S'))

        return datetime_list, cpu_list, ram_list


class AccessLog(object):

    @classmethod
    def get_list(cls,topn=10):
        _sql = 'select ip, url,code ,cnt from accesslog order by cnt desc limit %s'
        _args = (topn,)
        _count, _rt_list = MysqlConnection.execute_sql(_sql,_args)
        return _rt_list

    @classmethod
    def log2db(cls,logfile):
        # MysqlConnection.execute_sql('delete from accesslog;',(),False)
        fhandler = open(logfile,'r')

        rt_dict={}
        while True:
            line = fhandler.readline()
            if line == '':
                break
            nodes = line.split()
            ip, url, code = nodes[0], nodes[6], nodes[8]
            key = (ip, url, code)
            if key not in rt_dict:
                rt_dict[key] = 1
            else:
                rt_dict[key] = rt_dict[key] + 1
        fhandler.close()
        rt_list = []

        for _key, _cnt in rt_dict.items():
            rt_list.append(_key + (_cnt,))

        _sql = 'insert into accesslog(ip, url, code, cnt) values (%s, %s, %s, %s)'
        MysqlConnection.bulker_commit_sql(_sql,rt_list)

class Accesslog2(object):
    @classmethod
    def get_status_distribution(cls):
        _sql = 'select status, count(*) from accesslog2 group by status'
        _rt_cnt, _rt_list = MysqlConnection.execute_sql(_sql)
        _legends = []
        _datas = []

        _legends = [ _node[0] for _node in _rt_list]
        _datas = [dict(zip(("name","value"),_node))for _node in _rt_list]

        return _legends,_datas

    @classmethod
    def get_time_status_stack(cls):
        _sql="select DATE_FORMAT(logtime, '%%Y-%%m-%%d %%H:00:00') as ltime, status, count(*) from accesslog2 where logtime >= %s group by ltime, status;"
        _lasttime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-12*60*60))
        # _lasttime = '2014-08-23 00:00:00'
        print(_lasttime)
        _rt_cnt,_rt_list = MysqlConnection.execute_sql(_sql,(_lasttime,))
        _legends = []
        _xaxis = []
        _datas = []
        _temp_dict = {}

        for _ltime,_status,_cnt in _rt_list:
            if _status not in _legends:
                _legends.append(_status)
            if _ltime not in _xaxis:
                _xaxis.append(_ltime)
            _temp_dict.setdefault(_status,{})
            _temp_dict[_status][_ltime] = _cnt

        for _status,_stat in _temp_dict.items():
            _node={
                "name":_status,
                "type":'bar',
                "stack":'time_status_stack',
                "data":[]
            }


        for _status, _stat in _temp_dict.items():
            _node = {
                "name": _status,
                "type":'bar',
                "stack": 'time_status_stack',
                "data":[]
            }
            for _ltime in _xaxis:
                _cnt = _stat.get(_ltime, 0)
                _node['data'].append(_cnt)

            _datas.append(_node)

        print(_legends)
        print(_xaxis)
        print(_datas)
        return _legends, _xaxis, _datas

    @classmethod
    def get_access_map(cls):
        _server = '1.1.1.1'
        _server_addr = ''
        _server_lat = ''
        _server_lng = ''

        _geoCoord = {
            '上海': [121.4648, 31.2891],
            '北京': [116.4551, 40.2539],
            '大连': [122.2229, 39.4409],
            '广州': [113.5107, 23.2196]
        }
        _markLine = [
            [{"name": '上海', "value": 95}, {"name": '北京'}],
            [{"name": '广州', "value": 90}, {"name": '北京'}],
            [{"name": '大连', "value": 80}, {"name": '北京'}]
        ]
        _markPoint = [
            {"name": '上海', "value": 95},
            {"name": '广州', "value": 90},
            {"name": '大连', "value": 80}
        ]
        return _geoCoord, _markLine, _markPoint

if __name__=="__main__":
    AccessLog.log2db('/web/app/cmdb2/user/access_blog.log')




















