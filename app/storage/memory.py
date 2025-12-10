from typing import Dict, Any, Optional
import uuid
from threading import Lock

class InMemoryStore:
    def __init__(self):
        self.graphs: Dict[str, Dict[str, Any]] = {}
        self.runs: Dict[str, Dict[str, Any]] = {}
        self.lock = Lock()

    def save_graph(self, graph: Dict[str, Any]) -> str:
        graph_id = str(uuid.uuid4())
        with self.lock:
            self.graphs[graph_id] = graph
        return graph_id

    def get_graph(self, graph_id: str) -> Optional[Dict[str, Any]]:
        return self.graphs.get(graph_id)

    def create_run(self, graph_id: str, initial_state: Dict[str, Any]) -> str:
        run_id = str(uuid.uuid4())
        run = {
            "id": run_id,
            "graph_id": graph_id,
            "state": initial_state.copy(),
            "status": "pending"
        }
        with self.lock:
            self.runs[run_id] = run
        return run_id

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        return self.runs.get(run_id)


# global instance used by engine + API
store = InMemoryStore()
