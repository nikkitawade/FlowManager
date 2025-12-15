class FlowValidationError(Exception):
    pass
def validate_flow_json(flow_config):
    #Initial Flow JSON Validations
    if "flow" not in flow_config:
        raise FlowValidationError("Missing 'flow' key")
    flow = flow_config["flow"]

    #Flow Level Validations
    flow_keys = {"id", "name", "tasks", "conditions"}
    for key in flow_keys:
        if key not in flow and key != "start_task":
            raise FlowValidationError(f"Missing '{key}' in flow")

    #Task Level Validations   
    task_keys = {"name", "description"}
    for task in flow["tasks"]:
        for key in task_keys:
            if key not in task:
                if key == "description":
                    task["description"] = ""
                else:
                    raise FlowValidationError(f"Missing '{key}' in task '{task.get('name', 'unknown')}'")
    #Set default start_task if missing
    if "start_task" not in flow:
        flow["start_task"] = flow["tasks"][0]["name"]

    #Condition Level Validations
    condition_keys = {"source_task", "target_task_success", "target_task_failure", "outcome"}
    for condition in flow["conditions"]:
        for key in condition_keys:
            if key not in condition:
                raise FlowValidationError(f"Missing '{key}' in condition for source_task '{condition.get('source_task', 'unknown')}'")

