#!/usr/bin/python3
# script that generates a .tgz archive
# from the contents of the web_static
# folder of your AirBnB Clone repo, using the function do_pack.
from fabric.api import local
import os
from datetime import datetime


def do_pack():
    try:
        if not os.path.exists('versions'):
            os.mkdir("versions")
            Now = datetime.now()
            Date_And_Time = Now.strftime("%Y%m%d%H%M%S")
            local("tar -cvzf versions/web_static_{}.tgz web_static"
                  .format(Date_And_Time))
            return "versions/web_static_{}.tgz".format(Date_And_Time)
    except Exception:
        return None
