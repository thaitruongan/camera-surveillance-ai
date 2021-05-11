import paramiko
import os

local_path = "/home/anthai/Desktop/real-time-action-recognition/output/"
remote_path = "/root/Desktop/CameraAI/Record"

def send_vps():
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('103.77.160.29', username="root", password="25cMG81PqKyw")

    sftp = ssh.open_sftp()
    for root, dirs, files in os.walk(local_path):
        for fname in files:
            full_fname = os.path.join(root, fname)
            sftp.put(full_fname, os.path.join(remote_path, fname))

    sftp.close()
    ssh.close()