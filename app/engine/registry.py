from typing import Callable, Dict, Any, Optional

class ToolRegistry:
    
    def __init__(self):
        self._tools: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def register(self, name: str, fn: Callable[[Dict[str, Any]], Any]):
        self._tools[name] = fn

    def get(self, name: str) -> Optional[Callable[[Dict[str, Any]], Any]]:
        return self._tools.get(name)


tool_registry = ToolRegistry()
