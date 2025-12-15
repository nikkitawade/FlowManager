from task import TaskRegistry
from conditions import Condition
from validate_flow_json import validate_flow_json, FlowValidationError

#Create FlowManager class to manage flow execution
class FlowManager:
    def __init__(self, flow_config):
        #Validate flow JSON
        try:
            validate_flow_json(flow_config)
        except FlowValidationError as e:
            raise ValueError(f"Invalid flow JSON: {e}")
        #Store flow configuration
        self.flow = flow_config["flow"]

        #Create TaskRegistry instance to manage tasks and conditions
        self.task_registry = TaskRegistry(self.flow["tasks"], self.flow["conditions"])

    #Create run method to execute the flow
    def run(self):
        #Initialize current task to start_task
        current_task = self.flow["start_task"]
        execute,failure = [],[]
        #Loop through tasks until 'end' is reached
        while current_task != "end":
            try:
                print(f"\nRunning: {current_task}")
                #Get task object from registry
                task_obj = self.task_registry.get(current_task)
                if not task_obj:
                    return {"status": "failure", "error": f"Unknown task: {current_task}"}

                # Run task and get result
                result = task_obj.run()
                print(f"Result: {result['status']}")
                if result["status"] == "failure":
                    failure.append(current_task)
                else:
                    execute.append(current_task)
                current_task = result.get("next_task", "end")
            except Exception as e:
                print(f"Error occurred in task '{current_task}': {e}")
                failure.append(current_task)
                return {
                    "status": "failure",
                    "error": str(e),
                    "executed_tasks": execute
                }
        #Return final flow execution result    
        return {
            "status": result["status"],
            "executed_tasks": execute,
            "failed_tasks": failure
        }
