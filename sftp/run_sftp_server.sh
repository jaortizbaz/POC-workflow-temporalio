docker build -t repository-container .
docker run -d -p 22:22 docker.io/library/repository-container
