# SFTP
These are the instructions to run an instance of an SFTP in localhost using Docker.

## Run the SFTP container
```shell
cd ./sftp
docker build -t repository-container .
docker run -d -p 2222:22 docker.io/library/repository-container
```
Or run the script [run_sftp_server.sh](run_sftp_server.bat)

**Please find in the logs of the docker build the name of the container that needs to run.**

## Connect to the SFTP
For simplicity the password is set to **password**.

### Connect using a terminal
```shell
sftp -oPort=2222 sftp_user@localhost
```

### Connect using Filezilla or other client
| Field        | Value     |
|--------------|-----------|
| **Protocol** | SFTP      |
| **Host**     | localhost |
| **Port**     | 2222      |
| **User**     | sftp_user |
| **Password** | pswd      |

## External Links
[Create SFTP Container using Docker](https://medium.com/@lejiend7/create-sftp-container-using-docker-e6f099762e42)
