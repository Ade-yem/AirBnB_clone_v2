#!/usr/bin/python3
"""Create and distributes an archive to web servers"""
from os.path import exists
import time
from fabric.api import local
from fabric.operations import env, put, run
env.hosts = ['100.26.235.207', '54.86.208.71']
env.user = 'ubuntu'


def do_pack():
    """Generate an tgz archive from web_static folder"""
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".
              format(time.strftime("%Y%m%d%H%M%S")))
        return ("versions/web_static_{}.tgz".format(time.
                                                    strftime("%Y%m%d%H%M%S")))
    except:
        return None


def do_deploy(archive_path):
    """Distribute an archive to web servers"""
    if exists(archive_path) is False:
        return False

    try:
        file_name = archive_path.split("/")[-1]
        archive = ("/data/web_static/releases/" + file_name.split(".")[0])
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(archive))
        run("tar -xzf /tmp/{} -C {}".format(file_name, archive))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}/".format(archive, archive))
        run("rm -rf {}/web_static".format(archive))
        run('rm -rf /data/web_static/current')
        run("ln -s {} /data/web_static/current".format(archive))
        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """Create and distributes an archive to web servers"""
    try:
        path = do_pack()
        return do_deploy(path)
    except:
        return False
