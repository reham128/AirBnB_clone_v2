#!/usr/bin/python3
'''Fabric script (based on the file 1-pack_web_static.py) use do_deploy'''
from fabric.api import *
import os
from datetime import datetime


env.hosts = ["54.196.196.104", "100.25.102.27"]
env.user = "ubuntu"
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    '''to  generate .tgz archive of web_static folder'''
    try:
        local('mkdir -p versions')
        time_str = datetime.now().strftime('Y%m%d%H%M%S')
        local('tar -cvzf versions/web_static_{}.tgz web_static'
              .format(time_str))
        dir_path = f'versions/web_static_{time_str}.tgz'
        dir_size = os.path.getsize(dir_path)
        print(f'web_static packed: {dir_path} -> {dir_size}Bytes')

        return dir_path
    except OSError as e:
        print(f"Error creating archive: {e}")
        return (None)


def do_deploy(archive_path):
    '''to deploy web files to servers web-01, web-02'''
    if not os.path.exists(archive_path):
        return False
    try:
        archive_name = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_name)[0]

        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(archive_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_name, archive_no_ext))
        run("rm /tmp/{}".format(archive_name))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static"
            "/releases/{}/".format(archive_no_ext, archive_no_ext))

        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_no_ext))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
