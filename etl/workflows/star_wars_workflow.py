from datetime import timedelta
from temporalio import workflow

from etl.activity.sftp_activities import check_filename, SftpFile


@workflow.defn
class StarWarsEtl:
    @workflow.run
    async def run(self, filename: str) -> bool:
        file_received = await workflow.execute_activity(
            check_filename,
            SftpFile(filename),
            start_to_close_timeout=timedelta(seconds=10),
            heartbeat_timeout=timedelta(seconds=2),
        )

        return file_received


