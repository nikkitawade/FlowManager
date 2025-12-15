from fastapi import FastAPI, Request
from flow_manager import FlowManager
#Create FastAPI app instance
app = FastAPI()

@app.post("/")
#Create FlowManager instance and run the flow
def run_flow(body: dict): #convert Request to dict
    #Validate body exists
    if not body:
        return {"error": "No JSON body provided."}
    #Create object of FlowManager
    manager = FlowManager(body)
    #call run method of FlowManager
    result = manager.run()
    #Json response
    return result
