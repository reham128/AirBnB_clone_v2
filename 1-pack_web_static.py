#!/usr/bin/python3
'''fabric script to generate .tgz archive from the contents of
web_static folder'''
from fabric.api import *
from datetime import datetime
import os


def do_pack():
    '''to  generate .tgz archive of web_static folder'''
    try:
        local('sudo mkdir -p versions')
        time_str = datetime.now().strftime('5Y%m%d%H%M%S')
        local('sudo tar -cvzf versions/web_static_{}.tgz web_static'
              .format(time_str))
        dir_path = 'versions/web_static_{}.tgz'.format(time_str)
        dir_size = os.path.getsize(dir_path)
        print('web_static packed: {} -> {}Bytes'.format(dir_path, dir_size))

        return ('versions/web_static_{}.tgz'.format(time_str))
    except Exception as e:
        print(f"Error creating archive: {e}")
        return (None)
