# coding=utf-8
import logging
import os
import time

logdir = 'logs'


def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@singleton
class logger():
    def __init__(self):
        if not os.path.exists(logdir):
            os.mkdir(logdir)

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=logdir + '/nogizaka.log.' + time.strftime('%Y_%m_%d_%H'),
                            filemode='a'
                            )

        # 将DEBUG级别以上的日志输出屏幕
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d [%(levelname)s] %(message)s]')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        self.logging = logging