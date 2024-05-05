#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers."""
from fabric.api import local, put, run, env
from datetime import datetime
import os

env.hosts = ["54.196.196.104", "100.25.102.27"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    '''to  generate .tgz archive of web_static folder'''
    try:
        local('sudo mkdir -p versions')
        time_str = datetime.now().strftime('Y%m%d%H%M%S')
        local('sudo tar -cvzf versions/web_static_{}.tgz web_static'
              .format(time_str))
        dir_path = 'versions/web_static_{}.tgz'.format(time_str)
        dir_size = os.path.getsize(dir_path)
        print('web_static packed: {} -> {}Bytes'.format(dir_path, dir_size))

        return ('versions/web_static_{}.tgz'.format(time_str))
    except Exception as e:
        print(f"Error creating archive: {e}")
        return (None)


def do_deploy(archive_path):
    """Deploy the archive to the web servers."""
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
        print(f"Error deploying archive: {e}")
        return False


def deploy():
    """Create and distribute the archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
