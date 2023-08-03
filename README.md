# POC Temporal.io Python SDK
The goal of this project is to create a POC workflow that uses the Temporal Python SDK.

## Using Temporal.io in the project
1. Clone this repo
2. Make sure temporalio is in the file [pyproject.toml](pyproject.toml)

```text
temporalio = "1.2.0"
```

3. Install it as usual

```shell
poetry install
```

## How to run the workflow
1. Start the Temporal.io cluster.

    a. Using the CLI

    b. Using the cluster in localhost

2. Add the workflow from this project to temporal.io

### Temporal CLI 
Having the Temporal CLI installed in localhost:
1. Download the [Temporal CLI](https://temporal.download/cli/archive/latest?platform=windows&arch=amd64)
2. Unzip the file in a folder of your election
3. Add it to the Windows Environment Variables
4. Start the project using the command

```shell
temporal server start-dev
```

5. Go to http://localhost:8233

### Temporal cluster
1. Clone the project [temporalio-docker-compose](https://github.com/temporalio/docker-compose)
2. Open a Terminal in the location where the project was downloaded and start the cluster
```shell
docker compose up
```
3. Go to http://localhost:8080/

### Create namespaces
In order to isolate each project, we can create namespaces so that in the UI we have a clear overview of what is going
on. To do that we need to run the following command:

```shell
temporal operator namespace create <NAMESPACE_NAME>
```


### Add the workflow from this project to the existing cluster
Once the Temporal CLI or cluster is started we can just run the main module of the workflow.

**More details in the README file of each subproject.**

## External links
* [Temporal.io documentation](https://docs.temporal.io/)
* [All the ways to run a Temporal Cluster](https://docs.temporal.io/kb/all-the-ways-to-run-a-cluster)
* [Python SDK](https://docs.temporal.io/dev-guide/python)
* [Python SDK v2 example](https://github.com/temporalio/proposals/blob/master/python/phase-2.md)
* [Samples Python](https://github.com/temporalio/samples-python)
* [Documentation Samples Python](https://github.com/temporalio/documentation-samples-python)
