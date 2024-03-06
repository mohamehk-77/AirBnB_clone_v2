#!/usr/bin/python3
"""
script that generates a .tgz archive
from the contents of the web_static,
folder of your AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import local
import os
from datetime import datetime


def do_pack():
    """Function  to pack static files into an archive."""
    try:
        if not os.path.exists('versions'):
            os.mkdir("versions")
            Now = datetime.now()
            Date_And_Time = Now.strftime("%Y%m%d%H%M%S")
            Archive_Path = "versions/web_static_{}.tgz".format(Date_And_Time)
            local("tar -cvzf versions/web_static_{}.tgz web_static"
                  .format(Date_And_Time))
            local("chmod 660 {}".format(Archive_Path))
            return "versions/web_static_{}.tgz".format(Date_And_Time)
    except:
        return None
