import logging

from etl.config.config import Config
from etl.entity.sftp_properties import SftpProps

class Sftp:
    def __init__(self):
        config = Config()
        self.host = config.SFTP_HOST
        self.port = config.SFTP_PORT
        self.user = config.SFTP_USER
        self.password = config.SFTP_PASSWORD
        self.path = config.SFTP_PATH
        self.client = None
        self.sftp = None

    def __connect_sftp(self):
        from paramiko import SSHClient, AutoAddPolicy
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.user,
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

    def exists_file(self, sftp_props: SftpProps):
        print(f"Checking file {sftp_props.filename}.")
        try:
            self.__connect_sftp()
            for file in self.sftp.listdir(self.path):
                print(f"{file} is in the sftp")
                if file == sftp_props.filename:
                    return True
        except Exception as e:
            logging.error(f"Error checking file {sftp_props.filename}. Cause: {e}")
        finally:
            self.__disconnect_sftp()
        return False
