import logging

from etl.entity.sftp_properties import SftpProps


def __connect_sftp(sftp_props: SftpProps):
    from paramiko import SSHClient, AutoAddPolicy
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        client.connect(
            hostname=sftp_props.host,
            port=sftp_props.port,
            username=sftp_props.user,
            password=sftp_props.password)
    except Exception as error:
        raise RuntimeError(f"Error connecting to sftp server. Error: {error}")
    else:
        try:
            sftp = client.open_sftp()
        except Exception as error:
            raise RuntimeError(f"Error opening the SFTP. Error: {error}")
    return client, sftp


def __disconnect_sftp(client, sftp):
    if sftp:
        sftp.close()
    if client:
        client.close()


def exists_file(sftp_props: SftpProps):
    print(f"Checking file {sftp_props.filename}.")
    client = None
    sftp = None
    try:
        client, sftp = __connect_sftp(sftp_props)
        for file in sftp.listdir(sftp_props.path):
            print(f"{file} is in the sftp")
            if file == sftp_props.filename:
                return True
    except Exception as e:
        logging.error(f"Error checking file {sftp_props.filename}. Cause: {e}")
    finally:
        __disconnect_sftp(client, sftp)
    return False
