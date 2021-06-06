# _*_ coding:utf-8 _*_
import time

from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from threading import Lock
import psutil

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'D20fndvfMK27^313787-AQl131'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

name_space = '/test'


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # 获取系统时间
        cpus = psutil.cpu_percent(interval=None, percpu=True)
        # 获取系统cpu使用率 non-blocking
        print("发送第" + str(count) + "次数据：  CPUs:" + str(cpus) + " Time:" + t)
        socketio.emit('server_response',
                      {'data': [t, *cpus], 'count': count},
                      namespace='/test')


@app.route('/')
def get_abc():
    """demo page"""
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/push')
def push_once():
    """broadcast event generator"""
    return 'done!'


@socketio.on('connect', namespace=name_space)
def connected_msg():
    """socket client event - connected"""
    print('client connected!')
    global thread
    with thread_lock:
        if thread is None:
            print("开始获取数据")
            thread = socketio.start_background_task(target=background_thread)


@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    """socket client event - disconnected"""
    print('client disconnected!')


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=6008, debug=True)
