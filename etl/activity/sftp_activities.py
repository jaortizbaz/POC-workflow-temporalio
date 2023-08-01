import time
from temporalio import activity

from etl.entity.sftp_properties import SftpProps
from etl.repository.sftp import exists_file


@activity.defn
def check_filename(sftp_props: SftpProps) -> bool:
    activity.logger.info(f"Running activity to wait for file {sftp_props.filename}")

    while not exists_file(sftp_props):
        activity.heartbeat()
        print(f"The file does not exist yet in the SFTP. Waiting for file {sftp_props.filename}...")
        time.sleep(10)
    return True
