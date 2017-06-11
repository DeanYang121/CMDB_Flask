from flask import Flask
from flask import render_template
from flask import session
from flask import url_for
from flask import request
from flask import redirect
from flask import flash
import json
import gconf
from functools import wraps
from cmdb2.user import app
from models import User
from models import Asset
from models import IDC,AccessLog,Accesslog2
from models import Command,Performs
import time
from werkzeug import security
import os

def login_requried(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user') is None:
            return redirect('/')
        rt = func(*args,**kwargs)
        return rt
    return wrapper

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login/',methods=['POST'])
def login():

    username = request.form.get('username','')
    password = request.form.get('password','')
    _user = User.validate_login(username,password)
    print("_user:====",_user)
    if _user:
        session['user']=_user
        print('i am session:',session)
        return redirect('/users/')
    else:
        return render_template('login.html',username=username,error='用户名或密码错误')

@app.route('/user/charge-password/',methods=['POST'])
@login_requried
def change_passwd():
    user_id = request.form.get('userid','')
    manager_pwd = request.form.get('manager-password','')
    user_pwd = request.form.get('user-password','')
    is_ok,error=User.validate_change_password(user_id,manager_pwd,session['user']['username'],user_pwd)
    if is_ok:
        User.change_password(user_id,user_pwd)

    return json.dumps({"is_ok":is_ok,"error":error})

@app.route('/users/')
@login_requried
def users():
    users = []
    users = User.get_list()
    return render_template('users.html',users=users)

@app.route('/user/update/',methods=['POST'])
@login_requried
def update_user():
    user_id = request.form.get('userid','')
    username = request.form.get('update-username','')
    age = request.form.get('update-age','')
    is_ok,error = User.validate_change_info(user_id,username,age)
    if is_ok:
        User.change_info(user_id,age)
    return json.dumps({'is_ok':is_ok,'error':error})

@app.route('/user/delete/',methods=['GET'])
@login_requried
def delete_user():
    user_id = request.args.get('id','')
    User.delete(user_id)
    flash('用户删除成功！')
    return redirect('/users/')

'''添加用户'''
@app.route('/user/add/',methods=['POST'])
@login_requried
def add_user():
    username=request.form.get('username','')
    password=request.form.get('password','')
    age=request.form.get('age','')
    is_ok,error = User.validate_add_user(username,password,age)
    if is_ok:
        User.add_user(username,password,age)
    return json.dumps({'is_ok':is_ok,'error':error})

'''资产管理'''
@app.route('/assets/',methods=['GET','POST'])
@login_requried
def assets():
    _rt_lists=[]
    _rt_lists=Asset.get_list()
    idcs= IDC.get_list_dict()
    return render_template('assets.html',assets=_rt_lists,id_cs=idcs)

@app.route('/asset/create/')
@login_requried
def create_asset():
    return render_template('assets-create.html', id_cs=IDC.get_list_dict())

@app.route('/asset/add/', methods=['POST'])
@login_requried
def add_asset():
    _is_ok, _errors = Asset.validate_add(request.form)
    if _is_ok:
        Asset.add(request.form)
    return json.dumps({'is_ok' : _is_ok, 'errors' : _errors, 'success' : '添加成功'})


@app.route('/asset/modify/')
@login_requried
def update_asset():
    id = request.args.get('id','')
    return render_template('assets_modify.html',asset=Asset.get_by_key(id),idcs=IDC.get_list())

@app.route('/asset/update/',methods=['POST'])
@login_requried
def update_2_asset():
    _is_ok, _errors = Asset.validate_update(request.form)
    if _is_ok:
        Asset.update_asset(request.form)
    return json.dumps({'is_ok': _is_ok,'errors': _errors,'success':'更新成功'})

@app.route('/asset/delete/')
@login_requried
def delete_asset():
    id = request.args.get('id','')
    Asset.delete(id)
    return redirect('/assets/')

@app.route('/asset/cmd/')
@login_requried
def cmd():
    _id = request.args.get('id','')
    return render_template('assets-cmd.html',aid=_id)

@app.route('/asset/cmd_execute/',methods=['POST'])
@login_requried
def cmd_exe():
    _is_ok, _errors = Command.validate(request.form)
    _success = ''
    if _is_ok:
        _success = Command.execute(request.form)
    return json.dumps({'is_ok' : _is_ok, 'errors' : _errors, 'success' : _success})

@app.route('/asset/perform/')
@login_requried
def monitor():
    _id = request.args.get('id','')
    _asset=Asset.get_by_key(_id)
    datetime_list, cpu_list, ram_list = Performs.get_list(_asset['ip'])
    # datetime_list = ['2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50','2016-7-10 19:16:50', '2016-7-10 19:16:50', '2016-7-10 19:16:50']
    # cpu_list = [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
    # ram_list = [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
    return render_template('assets-monitor.html',datetime_list=json.dumps(datetime_list),
                                     cpu_list=json.dumps(cpu_list),ram_list=json.dumps(ram_list))

@app.route('/logs/')
@login_requried
def logs():
    topn = request.args.get('topn',10)
    topn = int(topn) if str(topn).isdigit() else 10
    return render_template('logs.html',rt_list=AccessLog.get_list(topn=topn))


@app.route('/uploadlogs/',methods=['POST'])
@login_requried
def update_log():
    # _file = request.form.get('logfile')
    UPLOAD_FOLDER = '/home/work/web/app/cmdb2/user/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    # _dirname = os.path.dirname(__file__)
    _file = request.files.get('logfile')
    print('sssq2323232',_file.filename)
    if _file:
        # _filepath = 'temp/%s'%time.strftime('%Y-%m-%d')
        _filepath = '{dirname}/{_time}-{fname}'.format(dirname=UPLOAD_FOLDER,_time=time.strftime('%Y-%m-%d'),fname=_file.filename)
        print(_filepath)
        _file.save(_filepath)
    return redirect('/logs/')

@app.route('/charts/')
@login_requried
def charts():
    status_legend, status_data = Accesslog2.get_status_distribution()
    time_status_legend, time_status_xaxis, time_status_data = Accesslog2.get_time_status_stack()
    _geoCoord, _markLine, _markPoint = Accesslog2.get_access_map()
    return render_template('charts.html',
            status_legend=json.dumps(status_legend), status_data=json.dumps(status_data),
            time_status_legend=json.dumps(time_status_legend), time_status_xaxis=json.dumps(time_status_xaxis), time_status_data=json.dumps(time_status_data),
            geoCoord=json.dumps(_geoCoord), markLine=json.dumps(_markLine), markPoint=json.dumps(_markPoint))


@app.route('/performs/',methods=['POST'])
def performs():
    _app_key = request.headers.get('app_key','')
    _app_secret = request.headers.get('app_secret','')
    #_app_key = request.args.get('app_key','')
    #app_secret = request.args.get('app_secret','')
    if _app_key != gconf.APP_KEY or _app_secret != gconf.APP_SECRET:
        return json.dumps({'code':400,'text':'secret error'})
    #获取json数据
    Performs.add(request.json)
    #0.10 request.get_json()
    return json.dumps({'code':200,'text':'success'})

"""注销登录"""
@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

