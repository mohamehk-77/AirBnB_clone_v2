#!/usr/bin/python3
"""
script that generates a .tgz archive
from the contents of the web_static,
folder of your AirBnB Clone repo, using the function do_pack.
"""
from os.path import isdir
from fabric.api import local, put, run, env
from datetime import datetime
from os.path import exists

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

"""
script (based on the file 1-pack_web_static.py) that distributes an archive
to your web servers, using the function do_deploy
"""


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        File_Base = archive_path.split('/')[1]
        File_Name = File_Base.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(File_Name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(File_Base, File_Name))
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/\
            releases/{}/'.format(File_Name, File_Name))
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(File_Name))
        run('rm /tmp/{}'.format(File_Base))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{} /data/web_static/current'
            .format(File_Name))

        print("New version deployed!")
        return True
    except:
        return False



def deploy():
    """
    Main deployment function.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
