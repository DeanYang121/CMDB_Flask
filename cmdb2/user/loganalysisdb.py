#encoding:utf-8
from dbutils import MysqlConnection

def get_topn(topn=10):
    _sql = 'select ip, url, code, cnt from accesslog order by cnt desc limit %s'
    _cnt, _rt_list = MysqlConnection.execute_sql(_sql, (topn, ))
    return _rt_list
