#!/usr/bin/python3
"""creates and distributes an archive to your web servers"""
from fabric.api import local, run, env, put
from os.path import exists
from datetime import datetime

env.hosts = ['100.26.235.207', '54.86.208.71']
env.user = 'ubuntu'


def deploy():
    """ distributes the archive to the web servers"""
    try:
        archive_path = do_pack()
    except Exception:
        return False
    return do_deploy(archive_path)


def do_pack():
    """packs flies to an archive"""
    try:
        if not exists('versions'):
            local('mkdir versions')
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{now}.tgz"
        local(f"tar -czvf {archive_path} web_static")
        return archive_path
    except Exceptions:
        return None


def do_deploy(archive_path):
    """Distribute an archive to web servers"""

    if not exists(archive_path):
        return False
    try:
        # Upload archive to /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        archive_file = archive_path.split("/")[-1]
        archive_name = archive_file.split(".")[0]
        remote_path = "/data/web_static/releases/{}".format(archive_name)
        run("sudo mkdir -p {}".format(remote_path))
        run("sudo tar -xzf /tmp/{} -C {}".
            format(archive_file, remote_path))
        run("sudo rm /tmp/{}".format(archive_file))
        run("sudo mv {}/web_static/* {}/".format(remote_path, remote_path))
        run("sudo rm -rf {}/web_static".format(remote_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(remote_path))
        print("New version deployed!")
        return True
    except Exception:
        return False
