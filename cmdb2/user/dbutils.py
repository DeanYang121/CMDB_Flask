#encondig:utf-8

import MySQLdb
import dbconf

class MysqlConnection(object):
    def __init__(self,host,user,passwd,port,db,charset,unix_socket):
        self.__host = dbconf.MYSQL_HOST
        self.__user = dbconf.MYSQL_USER
        self.__port = dbconf.MYSQL_PORT
        self.__passwd = dbconf.MYSQL_PASSWD
        self.__db = dbconf.MYSQL_DB
        self.__charset = dbconf.MYSQL_CHARSET
        self.__unix_socket =dbconf.Unix_socket
        self.__conn = None
        self.__cur = None
        self.__connect()

    def __connect(self):

        try:
            self.__conn = MySQLdb.connect(host=self.__host,port=self.__port,user=self.__user,db=self.__db,\
                                 passwd=self.__passwd,charset=self.__charset,unix_socket=self.__unix_socket)
            self.__cur = self.__conn.cursor()
        except BaseException as e:
            print(str(e))


    def execute(self,sql,args=()):
        _cnt = 0
        if self.__cur:
           _cnt = self.__cur.execute(sql,args)
        return _cnt

    def fetch(self,sql,args=()):
        _cnt = 0;
        _rt_list = []
        if self.__cur:
            _cnt = self.__cur.execute(sql,args)
            _rt_list = self.__cur.fetchall()
        return _cnt,_rt_list

    def commit(self):
        if self.__conn:
            self.__conn.commit()

    def close(self):
        if self.__cur:
            self.__cur.close()
            self.__cur = None
        if self.__conn:
            self.__conn.close()
            self.__conn = None

    @classmethod
    def execute_sql(cls,sql,args=(),fetch=True):
        _cnt = 0
        _rt_list = []

        _conn = MysqlConnection(host=dbconf.MYSQL_HOST,user=dbconf.MYSQL_USER,\
                                db=dbconf.MYSQL_DB,passwd=dbconf.MYSQL_PASSWD,\
                                port=dbconf.MYSQL_PORT,charset=dbconf.MYSQL_CHARSET,\
                                unix_socket = dbconf.Unix_socket
                                )

        if fetch:
            _cnt,_rt_list = _conn.fetch(sql,args)
        else:
            _cnt = _conn.execute(sql,args)
            _conn.commit()
        _conn.close()

        return _cnt,_rt_list

    @classmethod
    def bulker_commit_sql(cls,sql,args_lists=[]):
        _cnt = 0
        _rt_list = []
        _conn = MysqlConnection(host=dbconf.MYSQL_HOST,user=dbconf.MYSQL_DB,\
                                passwd=dbconf.MYSQL_PASSWD,port=dbconf.MYSQL_PORT,\
                                charset=dbconf.MYSQL_CHARSET,db=dbconf.MYSQL_DB, \
                                unix_socket=dbconf.Unix_socket
                                )
        for _args in args_lists:
            _cnt += _conn.execute(sql,_args)
        _conn.commit()

        return _cnt,_rt_list


if __name__=='__main__':
    # sql = 'select username,password from user where username=%s and password=md5(%s)'
    # args = ('dean','123456')
    # _cnt,_rt_list = MysqlConnection.execute_sql(sql,args)
    # print(_cnt)
    # print(_rt_list)
    _sql = "update user set password=md5(%s) where id = %s"
    user_pwd='111111'
    user_id='3'
    _args = ('111111','3')
    MysqlConnection.execute_sql(_sql, _args,False)











