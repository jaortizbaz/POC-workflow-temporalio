import time
from dataclasses import dataclass

from temporalio import activity

from etl.repository.sftp import SftpClient


@dataclass
class SftpFile:
    filename: str


@activity.defn
async def check_filename(sftp_file: SftpFile) -> bool:
    activity.logger.info("Running activity with parameter %s" % sftp_file.filename)
    sftp_client = SftpClient(
        host='localhost',
        port=2222,
        username='sftp_user',
        password='password',
        path='/'
    )

    while not sftp_client.exists(filename=sftp_file.filename):
        activity.heartbeat()
        time.sleep(10)
    return True
