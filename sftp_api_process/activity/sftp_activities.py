import time
from temporalio import activity

from sftp_api_process.entity.sftp_properties import SftpProps
from sftp_api_process.repository.sftp import Sftp


@activity.defn
def check_filename(sftp_props: SftpProps) -> bool:
    activity.logger.info(f"Running activity to wait for file {sftp_props.filename}")
    sftp = Sftp()
    while not sftp.exists_file(sftp_props):
        activity.heartbeat()
        print(f"The file does not exist yet in the SFTP. Waiting for file {sftp_props.filename}...")
        time.sleep(1)
    return True
