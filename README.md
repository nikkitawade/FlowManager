# FlowManager
Flow Manager Design

## Overview
This project implements a flow manager system where tasks are executed sequentially using Python and FastAPI. A JSON driven flow engine is executed. The system dynamically creates and executes task based on the predefined tasks configuration and condition in JSON File.


The focus of this assignment is on flow design, task dependency handling, validation and execution control rather than on implementing real data‑processing logic.

## Key Features

* JSON based flow definition
* Dynamic task creation at runtime
* Conditional task transitions based on task outcome
* JSON validation
* Clear separation of flow system (API, flow management, tasks, JSON validation)
* Supports sequential task execution until termination ("end")

## Project Structure

├── main.py                 # FastAPI entry point
├── flow_manager.py         # Flow manger logic
├── task.py                 # Dynamic task creation, task registry and condition check
├── validate_flow_json.py   # Flow JSON validation utility
└── README.md


## Flow Design

### 1. Task Dependency

* Tasks are executed sequentially starting from `start_task`.
* Each task decides the next task based on its execution result and the associated condition.
* Conditions are mapped using `source_task`.

### 2. Success / Failure Evaluation

* Each task returns:

  {
    "status": "success" | "failure",
    "next_task": "task_name" | "end"
  }

* The returned `status` is compared with the configured `outcome` in the condition.

### 3. Flow Behaviour

* **On success**: Execution proceeds to `target_task_success`
* **On failure**: Execution proceeds to `target_task_failure`
* **On exception**: Flow terminates and returns failure response

## Validation Logic

All input JSON is validated before execution:

### Flow‑level validation

* Required keys: `id`, `name`, `tasks`, `conditions`
* `start_task` defaults to the first task if missing

### Task‑level validation

* `name` is mandatory
* `description` is optional (defaults to empty string)

### Condition‑level validation

* Required keys:

  * `source_task`
  * `outcome`
  * `target_task_success`
  * `target_task_failure`

Validation errors raise a `FlowValidationError`.

### How to Execute the Project
1. Install Dependencies

pip install requirements.txt

2. Start the Application

From the project root directory, run:

uvicorn main:app --reload

The API will start at:

http://127.0.0.1:8000
3. Execute the Flow

Send a POST request to the root endpoint / with the flow JSON as the request body.

You can use Postman or any HTTP client.

Example using curl
curl --location 'http://127.0.0.1:8000/' \
--header 'Content-Type: application/json' \
--data '{
  "flow": {
    "id": "flow123",
    "name": "Data processing flow",
    "start_task": "task1",
    "tasks": [
      { "name": "task1", "description": "Fetch data" },
      { "name": "task2", "description": "Pre-Process data" },
      { "name": "task3", "description": "Process data" },
      { "name": "task4", "description": "Post-Process data" },
      { "name": "task5", "description": "Store data" }
    ],
    "conditions": [
      {
        "name": "condition_task1_result",
        "source_task": "task1",
        "outcome": "success",
        "target_task_success": "task2",
        "target_task_failure": "end"
      },
      {
        "name": "condition_task2_result",
        "source_task": "task2",
        "outcome": "success",
        "target_task_success": "task3",
        "target_task_failure": "end"
      },
      {
        "name": "condition_task3_result",
        "source_task": "task3",
        "outcome": "success",
        "target_task_success": "task4",
        "target_task_failure": "end"
      },
      {
        "name": "condition_task4_result",
        "source_task": "task4",
        "outcome": "success",
        "target_task_success": "task5",
        "target_task_failure": "end"
      }
    ]
  }
}
'
The response will include the execution status along with executed and failed tasks.
## API Usage

### Endpoint

```
POST /
```

### Request Body

Provide the flow definition JSON directly in the request body.

### Example Response

```json
{
  "status": "success",
  "executed_tasks": ["task1", "task2", "task3"],
  "failed_tasks": []
}
```

## Design Decisions

* Task logic is intentionally minimal (try–catch with default success)
* Emphasis is placed on flow management, error handling, and extensibility
* Tasks are created dynamically to support configurable workflows

## Assumptions

* Actual business logic (fetching, pre-processing, processing, post-processing and storing data) is out of scope for this assignment
* The system demonstrates how such logic would be plugged into the flow
* The design supports future enhancements such as:
  * Concurrent users
  * Real database operations
  * Asynchronous task execution

## Conclusion

This implementation demonstrates a clean, extensible approach to flow‑based task execution, focusing on structure, validation, and control flow. The design can be easily extended to support real‑world workloads and concurrent users.
