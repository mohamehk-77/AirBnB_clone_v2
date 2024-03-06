#!/usr/bin/python3
"""
script that generates a .tgz archive
from the contents of the web_static,
folder of your AirBnB Clone repo, using the function do_pack.
"""
from os.path import isdir
from fabric.api import local
from datetime import datetime


def do_pack():
    """Function  to pack static files into an archive."""
    try:
        Date_And_Time = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        Archive_Path = "versions/web_static_{}.tgz".format(Date_And_Time)
        local("tar -cvzf {} web_static".format(Archive_Path))
        return Archive_Path
    except:
        return None
