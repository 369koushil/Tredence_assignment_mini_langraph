from pydantic import BaseModel
from typing import Optional,List,Dict,Any

class NodeType(BaseModel):
    name:str
    fn:str
    
class EdgeType(BaseModel):
    from_node:str
    to_node:str
    condition:Optional[str]=None

class CreateGraphRequest(BaseModel):
    name:str
    nodes:List[NodeType]
    edges:List[EdgeType]
    start_node:str
    
class RunGraphRequest(BaseModel):
    graph_id:str
    initial_state:Dict[str,Any]
    