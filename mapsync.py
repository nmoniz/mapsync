#!/usr/bin/python

import sys
import traceback
import paramiko
import os
import subprocess
import re

CONFIG_MAP_PATH = 'mappath'
CONFIG_USER = 'user'
CONFIG_PASSWORD = 'password'
CONFIG_HOST = 'host'


def get_remote_md5(file, ssh):
    (ssh_in, ssh_out, ssh_err) = ssh.exec_command('md5sum "%s"' % file)
    for line in ssh_out.readlines():
        md5sum = line.split(" ")[0]
        return md5sum


def get_local_md5(file):
    local_out = subprocess.getoutput('md5sum "%s"' % file)
    return local_out.split(" ")[0]


def sync_files(sync_map, ssh, sftp):
    for pair in sync_map:
        sourcePath, destinationPath = pair.split(',')
        sourcePath = sourcePath.strip()
        destinationPath = destinationPath.strip()

        if get_remote_md5(destinationPath, ssh) != get_local_md5(sourcePath):
            print('> (' + str(os.path.getsize(sourcePath)) + ' Bytes) [' + re.search('([^/]+)$', sourcePath).group(0) + '] -> [' + destinationPath + ']')
            # send file
            sftp.put(sourcePath, destinationPath)
        else:
            # already synced, do not send file
            print('> [' + re.search('([^/]+)$', sourcePath).group(0) +  '] synced')


def read_map(file):
    with open(file) as mapFile:
        map = []

        for line in mapFile:
            if not line.startswith('#'):
                map.append(line)

        return map


def main():
    try:
        configs = {}

        #defaults
        configs[CONFIG_USER] = 'root'
        configs[CONFIG_PASSWORD] = ''
        configs[CONFIG_HOST] = 'localhost'

        #overide configs from args
        for arg in sys.argv:
            if ':' in arg:
                key, value = arg.split(':')
                configs[key] = value

        print('Connecting: ' + configs[CONFIG_USER] + '@' + configs[CONFIG_HOST])

        sshClient = paramiko.SSHClient()
        sshClient.load_system_host_keys()
        sshClient.connect(configs[CONFIG_HOST], 22, configs[CONFIG_USER], configs[CONFIG_PASSWORD])

        transport = paramiko.Transport((configs[CONFIG_HOST], 22))
        transport.connect(username=configs[CONFIG_USER], password=configs[CONFIG_PASSWORD])
        sftp = paramiko.SFTPClient.from_transport(transport)

        print('[ OK ]')

        print('Reading sync map: ' + configs[CONFIG_MAP_PATH])
        syncMap = read_map(configs[CONFIG_MAP_PATH])
        print('[ OK ]')

        print('Syncing: ' + str(len(syncMap)) + ' files')
        sync_files(syncMap, sshClient, sftp)
        print('[ OK ]')

        transport.close()
        sshClient.close()
    except Exception as e:
        print('[ ERROR ]')
        traceback.print_exc()


if __name__ == "__main__":
    main()
