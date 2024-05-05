#!/usr/bin/python3
'''creates and distributes an archive to your web servers,
using the function deploy'''
from fabric.api import *
from datetime import datetime
import os


env.hosts = ["54.196.196.104", "100.25.102.27"]


def do_pack():
    '''to  generate .tgz archive of web_static folder'''
    try:
        date_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{date_time_str}.tgz"

        if not path.exists("versions"):
            local("mkdir versions")

        local(f"tar -cvzf {archive_path} web_static")

        return archive_path

    except Exception as e:
        print(f"Error creating archive: {e}")
        return None


def do_deploy(archive_path):
    '''to deploy web files to servers web-01, web-02'''
    if not path.exists(archive_path):
        return False

    try:
        filename = path.basename(archive_path).split(".")[0]
        release_path = f"/data/web_static/releases/{filename}"

        print("Basename", path.basename(archive_path))
        put(archive_path, "/tmp/")

        run(f"mkdir -p {release_path}")
        run(f"tar -xzf /tmp/{path.basename(archive_path)} -C {release_path}")
        run(f"rm /tmp/{path.basename(archive_path)}")

        sudo(f"mv {release_path}/web_static/* {release_path}/")
        sudo("rm -rf /data/web_static/current")
        sudo(f"ln -s {release_path} /data/web_static/current")
        return True
    except Exception as e:
        return False


def deploy():
    '''Creates and distributes an archive to web servers web-01, web-02'''
    archive_path = do_pack()

    if archive_path is None:
        return False

    return do_deploy(archive_path)
