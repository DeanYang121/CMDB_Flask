#encoding: utf-8
import paramiko
import getpass

'''
手动连接ssh

客户端选择验证策略(服务器端密码策略)
ip, port, username
password/加载public key

操作

close

'''

def ssh_execute(host, username, password, cmds=[], port=22):
    _rt_list = []
    #创建ssh连接对象
    ssh = paramiko.SSHClient()

    #设置客户端登录验证方式
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #连接服务器信息
    ssh.connect(host, port, username, password)

    for _cmd in cmds:
        #操作
        stdin, stdout, stderr = ssh.exec_command(_cmd)
        #获取反馈信息
        _rt_list.append([_cmd, stdout.readlines(), stderr.readlines()])

    #关闭
    ssh.close()
    return _rt_list


def ssh_upload(host, username, password, files=[], port=22):
    try:
        t = paramiko.Transport((host, port))
        t.connect(username=username, password= password)
        sftp = paramiko.SFTPClient.from_transport(t)
        for _local, _remote in files:
            sftp.put(_local,_remote)
        print('文件上传成功！')
    except BaseException as e :
        print('文件上传失败！ 参考信息：%s'%str(e))
    finally:
        t.close()


if __name__ == '__main__':
    host = '192.168.196.144'
    port = 22
    username = 'root'
    password = getpass.getpass('please input password:')
    print ('"%s"' % password)
    cmds = [
                "echo 'hello i am dean'",
                'whoami'
            ]
    files = [('test.py', '/tmp/kk.py')]
    _rt_list = ssh_upload(host, username, password, files, port)
    _rt_list = ssh_execute(host, username, password, cmds, port)
    for _cmd, _out, _err in _rt_list:
        print(_cmd, _out, _err)