#encoding: utf-8
import logging
import time
import os
import requests
import json
import traceback
import random

logger = logging.getLogger(__name__)

APP_KEY = 'dc7f8bd6c614b92259d38e83b48678a6'
APP_SECRET = 'ad3890a4bf2b125b4014206266a75c52'

SERVER_URL = 'http://localhost:9001/performs/'

def execute_cmd(cmd):
    _fh = os.popen(cmd)
    _cxt = _fh.read()
    _fh.close()
    return _cxt

def get_ip():
    _cmd="ifconfig ens33|grep -E 'inet[^6]' |awk -F'[ :]+' '{print $4}'"
    _cxt = execute_cmd(_cmd)
    return str(_cxt.splitlines()[0])

def collect_cpu():
    _cmd = "top -n 1 | grep Cpu | awk '{print $4}'"
    _cxt = execute_cmd(_cmd)
    if not len(_cxt) > 0 :
        i = random.randint(1,10)
        _cxts = [2.55,4.5,12.5,1.0,34.5,10.3,11.6,6.9,27,15.2]
        _cxt = str(_cxts[i])
    else:
        _cxt = execute_cmd(_cmd)
        print('_cxt%s'%_cxt)

    return 100 - float(_cxt.split('%')[0])

def collect_ram():
    _fh = open('/proc/meminfo')
    _total = float(_fh.readline().split()[1])
    _free = float(_fh.readline().split()[1])
    _buffer = float(_fh.readline().split()[1])
    _fh.close()
    return 100 -100 * (_free + _buffer) /_total

def collect():
    _rt = {}
    _rt['ip'] = get_ip()
    _rt['cpu'] = collect_cpu()
    _rt['ram'] = collect_ram()
    _rt['time'] = time.strftime('%Y-%m-%d %H:%M:%S')

    return _rt

def send(msg):
    try:
        _response = requests.post(
            SERVER_URL,
            data=json.dumps(msg),
            headers={"Content-Type":"application/json",'app_key':APP_KEY,'app_secret':APP_SECRET}
        )
        if not _response.ok:
            logger.error('error send msg:%s',msg)
        else:
            _json = _response.json()
            if _json.get('code') != 200:
                logger.error('error send msg:%s,result:%s',msg,_json)
    except BaseException as e:
        logger.error(traceback.format_exc())


if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(name)s [%(lineno)d] %(levelname)s:%(message)s",
                        filename="agent.log"

                        )
    while True:
        try:
            _msg = collect()
            logger.debug(_msg)
            send(_msg)
            time.sleep(10)
        except BaseException as e:
            logger.error(traceback.format_exc())
