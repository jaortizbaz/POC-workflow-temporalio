# Hello world
This is the simplest project we can create in Temporal. 

## Components
This project has the following components:
1. [Dataclass](#Dataclass)
2. [Activity](#Activity)
3. [Workflow](#Workflow)
4. [Main](#Main)

### [Dataclass](compose_greeting_input.py)
This is an example of a type of data that can be used in an Activity in Temporal:

```python
@dataclass
class ComposeGreetingInput:
    greeting: str
    name: str
```

### [Activity](activity/compose_greeting_activity.py)
An activity can be any piece of code in Python. In this case it is just a function which returns a string with a
greeting and a name which are past as a parameter of [ComposeGreetingInput](compose_greeting_input.py):

```python
@activity.defn
async def compose_greeting(greeting_input: ComposeGreetingInput) -> str:
    activity.logger.info("Running activity with parameter %s" % greeting_input)
    return f"{greeting_input.greeting}, {greeting_input.name}!"
```

### [Workflow](workflow/greeting_workflow.py)
The workflow is the set of tasks that needs to run in the project. In this case we have a workflow composed by only one
activity:

```python
@workflow.defn 
class GreetingWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            compose_greeting,
            ComposeGreetingInput("Hello", name),
            start_to_close_timeout=timedelta(seconds=10),
        )
```

This workflow is running the activity **compose_greeting** using as input a new **ComposeGreetingInput** object with a
greeting and a name that was past as a parameter, and, finally, setting a timeout of 10 seconds.

### [Main](hello_world_main.py)
In the main module we have the following components:
* a client that connects to the Temporal engine and that will run the project.
* a Worker which is the resource where the workflow.
* the execution of the workflow.

```python
async def main():
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="hello-activity-task-queue",
        workflows=[GreetingWorkflow],
        activities=[compose_greeting],
    ):
        result = await client.execute_workflow(
            GreetingWorkflow.run,
            "World",
            id="hello-activity-workflow-id",
            task_queue="hello-activity-task-queue",
        )
        print(f"Result: {result}")
```

To execute the workflow, here we added a name which the workflow expects as a parameter (World in this case). Also, they
are needed:
* id: the unique identifier of the workflow. **This is not the instance ID**
* task_queue: the queue where this instance of the task is going to be queued until it is executed.

## Run the workflow
To run the workflow run the file [hello_world_main.py](hello_world_main.py).

After some seconds it should appear the message **Hello, World!** in the console.
