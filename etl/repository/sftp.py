import logging

import paramiko


class SftpClient:

    def __init__(self, host, port, username, password, path):
        self.client = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.path = path

    def __connect_sftp(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password)
        except Exception as error:
            raise RuntimeError(f"Error connecting to sftp server. Error: {error}")
        else:
            try:
                self.sftp = self.client.open_sftp()
            except Exception as error:
                raise RuntimeError(f"Error opening the SFTP. Error: {error}")

    def __disconnect_sftp(self):
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()

    def exists(self, filename):
        try:
            self.__connect_sftp()
            for file in self.sftp.listdir(self.path):
                if file == filename:
                    return True
        except Exception as e:
            logging.info(f"Error checking file {filename}. Cause: {e}")
        return False
