# POC Temporal.io Python SDK
The goal of this project is to create a POC workflow that uses the Temporal Python SDK.

## Using Temporal.io in the project
1. Add the dependency in the requirements.txt file
```text
temporalio==1.2.0
```
2. Install it as usual
```shell
./venv/Scripts/pip intall -r requirements.txt
```

## Develop a workflow


## How to run the workflow
1. Run the SFTP
2. Start the Temporal.io cluster.

    a. Using the CLI

    b. Using the cluster in localhost

3. Add the workflow from this project to temporal.io

### Run the SFTP
To run an instance of a SFTP in localhost using Docker please follow [these instructions](sftp/README.md).

### Temporal CLI 
Having the Temporal CLI installed in localhost:
1. Download the [Temporal CLI](https://temporal.download/cli/archive/latest?platform=windows&arch=amd64)
2. Unzip the file in a folder of your election
3. Add it to the Windows Environment Variables
4. Start the project using the command
```shell
temporal server start-dev
```

### Temporal cluster
1. Clone the project [temporalio-docker-compose](https://github.com/temporalio/docker-compose)
2. Open a Terminal in the location where the project was downloaded and start the cluster
```shell
docker compose up
```

### Add the workflow from this project to the existing cluster


## External links
* [Temporal.io documentation](https://docs.temporal.io/)
* [All the ways to run a Temporal Cluster](https://docs.temporal.io/kb/all-the-ways-to-run-a-cluster)
* [Python SDK](https://docs.temporal.io/dev-guide/python)