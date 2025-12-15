class BaseTask:
    def run(self):
        raise NotImplementedError("Task must implement run() method")

    #Create Task Dynamically
    def create_dynamic_task(name, description,condition=None):
        try:
            #Dynamic run method
            def run(self):
                try:
                    print(f"Running sequential task: {name} | {description}")

                    # if task == "task3":
                    #     status="failure"
                    # else:
                    #     status = "success"
                    status = "success"

                    #check condition if exists
                    if condition:
                        if condition["outcome"] == status:
                            next_task = condition["target_task_success"]
                        else:
                            next_task = condition["target_task_failure"]
                    else:
                        next_task = "end"
                    print(f"Task '{name}' completed with status: {status}, next task: {next_task}")
                    return {"status": status, "next_task": next_task}
                except Exception as e:
                    return {"status": "failure", "next_task": "end", "error": str(e)}

            #Create task classes dynamically
            DynamicTask = type(name, (BaseTask,), {"run": run})
            return DynamicTask

        except Exception as e:
            print("Error creating task:", e)
            return None

#Create TaskRegistry to manage tasks
class TaskRegistry:
    def __init__(self, task_list, condition_list):
        self.tasks = task_list
        self.conditions = condition_list
        #Create map for source_task to condition
        self.condition_map = {c["source_task"]: c for c in condition_list}
        self.registry = {}

        #Iterate through tasks and create dynamic task classes
        for t in self.tasks:
            name = t["name"]
            desc = t["description"]
            cond = self.condition_map.get(name)
            #Create dynamic task class with condition if exists
            task_class = BaseTask.create_dynamic_task(name, desc, cond)
            #Map task name to task class instance
            self.registry[name] = task_class()

    def get(self, task_name):
        return self.registry.get(task_name)
    
    def run(self):
        print("This is a static task.")
        return {"status": "success"}