FROM ubuntu:16.04

RUN apt-get update && apt-get install -y openssh-server

# configure repository user
RUN useradd -rm -d /home/sftp_user -s /bin/bash -G sudo -u 10001 sftp_user
RUN echo "sftp_user:pswd" | chpasswd

# necessary sshd file
RUN mkdir /var/run/sshd

# SSH login fix (Keeping Session Alive). If not, user will be kick off after ssh
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

#setup directory for repository
RUN mkdir -p /var/repository/uploads
RUN chown root:root /var/repository
RUN chmod 755 /var/repository
RUN chown sftp_user:sftp_user /var/repository/uploads
