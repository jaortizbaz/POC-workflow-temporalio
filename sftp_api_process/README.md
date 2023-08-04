# SFTP API PROCESS
This project has two main modules:

1. [Worker](worker_main.py)

    This module will create the worker where the workflow tasks will be running. Actually, the logs of the workflows
    will appear in the console of the execution of this module.

2. [Workflow](workflow_main.py)
    
    In this module the workflows will be started and run. For this project, we have created two workflows:

   1. [SFTP workflow](#SFTP workflow)
   2. [API workflow](#API workflow)

## [SFTP workflow](workflows/sftp_workflow.py)
This workflow calls an activity which is pooling the SFTP until it receives the expected file.

Once that file is in the SFTP, it sends a signal to the [API workflow](workflows/star_wars_workflow.py).
```python
handle = workflow.get_external_workflow_handle_for(StarWarsWorkflow.run, workflow_id=sftp_workflow_props.workflow_id)
await handle.signal(StarWarsWorkflow.set_has_file, file_received)
```

## [API workflow](workflows/star_wars_workflow.py)
This workflow gets information about Star Wars characters using the public API [swapi](https://swapi.dev/api/). To do
that, it receives an ID of a person and then it runs 3 activities:

- The first activity is just waiting for the SFTP to send the signal saying that the file is already in the SFTP and to
    trigger the start of this workflow:

- The second activity is calling the API [swapi](https://swapi.dev/api/) using the ID that was received as a parameter.

- And finally, the third activity will run only if the ID received is an even number, and it will get the planet
  information of the character received for the ID past as a parameter.

As mentioned above, this workflow receives signals from external sources. To do that, we followed these steps:
1. define the attribute in the constructor of the module:
    ```python
    def __init__(self):
        self._has_file = None
    ```
   
2. create a function which updates the value of the attribute:
    ```python
    @workflow.signal
    async def set_has_file(self, has_file):
        self._has_file = has_file
    ```
   
3. and, during the execution, waits for the signal to be received:
    ```python
    await workflow.wait_condition(lambda: self._has_file is not None)
    ```

Apart from this, we have defined a query parameter which is mean to allow the workflow runner to access the result of
the execution of the workflow even when this has finished.

1. define the attribute in the constructor of the module:
    ```python
    def __init__(self):
        self._star_wars_details = None
    ```

2. create a function which returns the value of the attribute:
    ```python
    @workflow.query
    async def get_star_wars_details(self):
        return self._star_wars_details
    ```

3. update the value of the attribute in the run of the workflow:
    ```python
    self._star_wars_details = {
        "person": star_wars_person_data,
        "planet": star_wars_planet_data
    }
    ```

4. query the data from the workflow runner:
    ```python
    handle = await client.start_workflow(
        workflow=StarWarsWorkflow.run,
        arg=person_id,
        id=star_wars_workflow_id,
        task_queue=config.TASK_QUEUE_NAME,
    )
    await handle.result()
    result = await handle.query(StarWarsWorkflow.get_star_wars_details)
    print(f"Result: {result}")
    ```

## Configuration
Please find below an example of the environment variables values for this project:
```text
API_BASE_URL=https://swapi.dev/api/

SFTP_HOST=localhost
SFTP_PORT=2222
SFTP_USER=sftp_user
SFTP_PASSWORD=pswd
SFTP_PATH=/var/repository/uploads
SFTP_FILEPATTERN=file_star_wars.csv

TEMPORALIO_HOST=localhost:7233
TASK_QUEUE_NAME=star_wars_task_queue
SFTP_WORKFLOW_ID=poc-sftp-wf
STAR_WARS_WORKFLOW_ID=poc-star-wars-wf

PEOPLE_LIST=1,2,3,4,5
```
