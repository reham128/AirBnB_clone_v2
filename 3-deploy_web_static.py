#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers."""
from fabric.api import local, put, run, env
from datetime import datetime
import os
from os.path import exists, isdir
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
    """distributes an archive to the web servers"""
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("New version deployed!")
        return True

    return False


def deploy():
    """Create and distribute the archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
