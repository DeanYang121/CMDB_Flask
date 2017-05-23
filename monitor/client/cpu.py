#apt install sysstat
import subprocess
import os

def execute_cmd(cmd):
    _fh = os.popen(cmd)
    _cxt = _fh.read()
    _fh.close()
    return _cxt

def monitor(frist_invoke=1):
    shell_command = "top -bn 1 |grep Cpu|awk '{print $2,$4,$6,$8,$10,$16}'"
    # result = subprocess.Popen("top -n 1 |grep Cpu|awk '{print $2,$4,$6,$8,$10,$16}'",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    result = execute_cmd(shell_command)
    # print(result.stdout.read())
    # print(result.stderr.read())  result.stderr.read() == None
    # print(result)
    shell_ip = "ifconfig ens33|grep -E 'inet[^6]' |awk -F'[ :]+' '{print $4}'"
    result_ip = subprocess.Popen(shell_ip,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    ip = result_ip.stdout.read()
    if len(ip) == 0 :
        ip = result_ip.stderr.read()
    if not len(result) >= 0:
        value_dic ={'status':result.stderr.read(),'result':result}
    else:
        value_dic ={}
        user,system,nice,idle,iowait ,steal = list(result.split())
        # print(user,nice,system,iowait,steal,idle)
        value_dic = {
            "ip":ip,
            'user':user,
            'system': system,
            'nice':nice,
            'idle':idle,
            'iowait':iowait,
            'steal':steal
        }
    return value_dic
        # print(value_dic)

if __name__=="__main__":
    monitor()
