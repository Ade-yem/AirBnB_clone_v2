#!/usr/bin/python3
"""Create a compressed archive of the web_static folder"""
from fabric.api import local, env
from datetime import datetime
import os

env.hosts = ['localhost']  # set the target hosts


def do_pack():
    """Create a compressed archive of the web_static folder"""
    try:
        # create the folder if it doesn't exist
        if not os.path.exists("./versions"):
            os.mkdir("./versions")

        now = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "web_static_" + now + ".tgz"
        local("tar -czvf versions/{} web_static".format(filename))
        return "versions/{}".format(filename)
    except Exception:
        return None
