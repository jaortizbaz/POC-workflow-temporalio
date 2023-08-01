from os import environ


class Config:
    @staticmethod
    def __set_env_var_if_exist(varname):
        if varname in environ:
            return environ[varname]
        return ''

    def __init__(self):
        self.TEMPORALIO_HOST = self.__set_env_var_if_exist("TEMPORALIO_HOST")
        self.SFTP_HOST = self.__set_env_var_if_exist("SFTP_HOST")
        self.SFTP_PORT = int(self.__set_env_var_if_exist("SFTP_PORT"))
        self.SFTP_USER = self.__set_env_var_if_exist("SFTP_USER")
        self.SFTP_PASSWORD = self.__set_env_var_if_exist("SFTP_PASSWORD")
        self.SFTP_PATH = self.__set_env_var_if_exist("SFTP_PATH")
        self.SFTP_FILEPATTERN = self.__set_env_var_if_exist("SFTP_FILEPATTERN")
