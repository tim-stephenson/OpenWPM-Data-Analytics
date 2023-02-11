

from typing import Any
from analyzers.static_analyzer import Static_Analyzer


class Canvas1MDynamic(Static_Analyzer):
    
    def fingerprinting_type(self) -> str:
        return "Canvas"
    
    def _classify(self) -> bool:
        return True

    def _reset(self) -> bool:
        return True

    def _read_row(self, row : Any) -> None:
        pass