#!/usr/bin/python3
""" distributes an archive to your web server"""
from fabric.api import local, env, run, put
from os.path import exists
from datetime import datetime

env.hosts = ['100.26.235.207', '54.86.208.71']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

def do_deploy(archive_path):
    """Distribute an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        # Create directory to uncompress the archive
        archive_file = archive_path.split("/")[-1]
        archive_name = archive_file.split(".")[0]
        remote_path = "/data/web_static/releases/{}".format(archive_name)
        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}".
            format(archive_file, remote_path))
        run("rm /tmp/{}".format(archive_file))
        run("mv {}/web_static/* {}/".format(remote_path, remote_path))
        run("rm -rf {}/web_static".format(remote_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_path))
        print("New version deployed!")
        return True
    except Exception:
        return False
