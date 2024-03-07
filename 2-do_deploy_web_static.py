#!/usr/bin/python3
"""
script (based on the file 1-pack_web_static.py) that distributes an archive
to your web servers, using the function do_deploy
"""
from fabric.api import run, put, env
from os.path import exists

env.hosts = ['100.26.173.131', '54.90.9.164']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        F_N = archive_path.split("/")[-1]
        N_Ext = file_n.split(".")[0]
        File_Path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(File_Path, N_Ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(F_N, File_Path, N_Ext))
        run('rm /tmp/{}'.format(F_N))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(File_Path, N_Ext))
        run('rm -rf {}{}/web_static'.format(File_Path, N_Ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(File_Path, N_Ext))
        return True
    except:
        return False
