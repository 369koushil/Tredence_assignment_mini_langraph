from fastapi import FastAPI, HTTPException
import asyncio
from app.workflows.data_quality import get_data_quality_workflow
from app.models.schema import GraphCreateRequest, GraphRunRequest
from app.storage.memory import store
from app.engine.graph_engine import GraphEngine
from fastapi import WebSocket, WebSocketDisconnect
from app.engine.ws_manager import ws_manager


app = FastAPI()

engine = GraphEngine()


# create a custom graph
@app.post("/graph/create")
async def create_graph(req: GraphCreateRequest):
    graph = {
        "name": req.name,
        "nodes": [n.dict() for n in req.nodes],
        "edges": [e.dict() for e in req.edges],
        "start_node": req.start_node
    }

    graph_id = store.save_graph(graph)
    return {"graph_id": graph_id}


# creates example data quality workflow
@app.post("/graph/create_example/data_quality")
async def create_data_quality_graph():
    graph = get_data_quality_workflow()
    graph_id = store.save_graph(graph)
    return {"graph_id": graph_id}


# run workflow
@app.post("/graph/run")
async def run_graph(req: GraphRunRequest):
    graph = store.get_graph(req.graph_id)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")

    run_id = store.create_run(req.graph_id, req.initial_state)

    print("AFTER CREATING RUN → store.runs =", store.runs)

    asyncio.create_task(engine.run(req.graph_id, run_id))
    return {"run_id": run_id, "status": "started"}


# get workflow run state
@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    print("REQUESTED RUN ID:", run_id)
    print("ALL RUNS IN STORE:", store.runs)

    run = store.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    return {
        "run_id": run_id,
        "status": run["status"],
        "state": run["state"]
    }


# real time logging using web sockets
@app.websocket("/ws/logs/{run_id}")
async def websocket_logs(websocket: WebSocket, run_id: str):
    await ws_manager.connect(run_id, websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        ws_manager.disconnect(run_id, websocket)
