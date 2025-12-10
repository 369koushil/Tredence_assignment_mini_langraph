import asyncio
from typing import Dict, Any, List, Optional
from app.storage.memory import store
from app.engine.registry import tool_registry
from app.engine.ws_manager import ws_manager


def evaluate_condition(expr: str, state: Dict[str, Any]) -> bool:
    try:
        return bool(eval(expr, {"__builtins__": {}}, {"state": state}))
    except Exception:
        return False


class GraphEngine:
    

    def __init__(self):
        pass

    async def run(self, graph_id: str, run_id: str):
        graph = store.get_graph(graph_id)
        run = store.get_run(run_id)

        if graph is None or run is None:
            return

        state = run["state"]
        run["status"] = "running"

        current_node: Optional[str] = graph.get("start_node")
        step_count = 0
        max_steps = 500

        while current_node is not None and step_count < max_steps:
            step_count += 1

            await ws_manager.send(run_id, {"event": "node_start", "node": current_node})

            node_def = self._find_node(graph.get("nodes", []), current_node)
            if node_def is None:
                break

            fn_name = node_def.get("fn")
            fn = tool_registry.get(fn_name)
            if fn is None:
                break

            try:
                result = fn(state)
                if asyncio.iscoroutine(result):
                    await result
            except Exception:
                break

            await ws_manager.send(
                run_id,
                {
                    "event": "node_end",
                    "node": current_node,
                    "state": state
                }
            )

            next_node = self._find_next_node(graph.get("edges", []), current_node, state)

            if next_node is None:
                current_node = None
                break

            if next_node == graph.get("start_node"):
                await ws_manager.send(
                    run_id,
                    {
                        "event": "loop_iteration",
                        "iteration": step_count
                    }
                )

            current_node = next_node
            await asyncio.sleep(0)

        await ws_manager.send(run_id, {"event": "completed"})
        run["status"] = "completed"

    def _find_node(self, nodes: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
        for n in nodes:
            if n.get("name") == name:
                return n
        return None

    def _find_next_node(self, edges: List[Dict[str, Any]], current: str, state: Dict[str, Any]) -> Optional[str]:
        for edge in edges:
            if edge.get("from_node") != current:
                continue

            cond = edge.get("condition")
            if not cond:
                return edge.get("to_node")

            if evaluate_condition(cond, state):
                return edge.get("to_node")

        return None
