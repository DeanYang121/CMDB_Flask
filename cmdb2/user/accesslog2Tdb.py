#encoding: utf-8
import time
from geoip2 import database
from dbutils import MysqlConnection

if __name__=='__main__':
    logfile='/web/app/cmdb2/user/access_blog.log'
    MysqlConnection.execute_sql('delete from accesslog2;',(),False)
    reader = database.Reader('GeoLite2-City.mmdb')
    fhander = open(logfile,'r')

    rt_list = []
    while True:
        line = fhander.readline()
        if line == '':
            break

        nodes = line.split()
        ip,logtime,url,status = nodes[0],nodes[3][1:],[6],[8]
        logtime = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(logtime,'%d/%b/%Y:%H:%M:%S'))
        try:
            response = reader.city(ip)
            if 'China' != response.country.name:
                print('ip not in china:%s'%ip)
                continue
            city = response.city.name.get('zh-CN','')
            if city == '':
                print('ip city is empty:%s'%ip)
                continue

            lat = response.location.latitude
            lng = response.location.longitude
            rt_list.append((logtime,ip,url,status,lat,lng,city))
        except BaseException as e:
            print('geo ip not found ip:%s'%ip)

    fhander.close()
    reader.close()

    _sql = 'insert into accesslog2(logtime, ip, url, status, lat, lng, city) values (%s, %s, %s, %s, %s, %s, %s)'
    MysqlConnection.bulker_commit_sql(_sql)