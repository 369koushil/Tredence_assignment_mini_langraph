from pydantic import BaseModel
from typing import Optional,Dict,Any,List


class NodeDef(BaseModel):
    name: str
    fn: str


class EdgeDef(BaseModel):
    from_node: str
    to_node: str
    condition: Optional[str] = None


class GraphCreateRequest(BaseModel):
    name: str
    nodes: List[NodeDef]
    edges: List[EdgeDef]
    start_node: str


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]
