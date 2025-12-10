# Agent Workflow Engine (FastAPI)

This project implements a small graph execution engine using FastAPI. The engine supports node-based execution, shared state updates, conditional branch transitions, looping, and asynchronous execution. A WebSocket endpoint is included for simple real-time log streaming.

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the server

```bash
uvicorn app.main:app
```

### 3. Open API documentation

```
http://127.0.0.1:8000/docs
```

---

## Project Structure

```
app/
  main.py
  engine/
    graph_engine.py
    registry.py
    ws_manager.py
  storage/
    memory.py
  models/
    schema.py
  tools/
    data_quality_tools.py
  workflows/
    code_review.py
    data_quality.py
```

---

## What the Workflow Engine Supports

### • Nodes

Each node is a Python function that reads and modifies a shared state.

### • Shared State

State is a dictionary passed across nodes through the workflow.

### • Edges and Transitions

Edges define execution flow. Optional conditions enable branching and looping.

### • Looping

Workflows may repeat sections until a state condition is satisfied.

### • Async Execution

Workflows run asynchronously using background tasks.

### • WebSocket Log Streaming (Optional Feature)

A simple WebSocket endpoint is provided to stream node-by-node execution logs in real time.

### • Example Workflows Included

1. **Data Quality Pipeline**

---

## Example Endpoints

### Create Example Workflow

```
POST /graph/create_example/data_quality
```

### Run a Workflow

```
POST /graph/run
```

Body:

```json
{
  "graph_id": "...",
  "initial_state": { "key": "value" }
}
```

```
example
```
```json
{
  "graph_id": "a72d2e0a-60a2-4443-ba0e-8de6f8b41f8b",
   "initial_state": {
    "data": [10, 12, 111, 113, 10, 91, 12],
    "threshold": 0.2
  }
}
```


### Check Workflow State

```
GET /graph/state/{run_id}
```

### Connect to WebSocket Logs

```
ws://127.0.0.1:8000/ws/logs/{run_id}
```

---

## What I Would Improve With More Time

* Persistent storage instead of in-memory store.
* Better condition evaluator with a safe expression parser.
* A small frontend to visualize workflow execution.

---
