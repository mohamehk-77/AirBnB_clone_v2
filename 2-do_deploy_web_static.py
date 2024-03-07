#!/usr/bin/python3
"""
script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers,
using the function do_deploy
"""
from fabric.api import *
from os.path import exists

env.hosts = ['100.26.173.131', '54.90.9.164']

def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if not exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        File_Base = archive_path.split('.')[0].split('/')[-1]
        run('mkdir -p /data/web_static/releases/{}'.format(File_Base))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}'.format(File_Base, File_Base))
        run('rm /tmp/{}.tgz'.format(File_Base))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(File_Base))
        return True
    except:
        return False

