from typing import Set, List, Any
from sqlalchemy.engine import Engine
import logging
from analyzers.static_analyzer import Static_Analyzer
from utils.grep_utils import grepForKeywords


class WebGL_Static(Static_Analyzer):

    def __init__(self, engine : Engine, db : Any, logger : logging.Logger) -> None:
        self.__keywords : List[str] = ["WEBGL_debug_renderer_info","UNMASKED_VENDOR_WEBGL","UNMASKED_RENDERER_WEBGL"]
        super().__init__(engine,db,logger)

    @staticmethod
    def fingerprinting_type() -> str:
        return "WebGL"
    
    def _analyze_one(self,source_code : str) -> bool:
        results: Set[str] = grepForKeywords(self.__keywords, source_code)        
        return results.__contains__("WEBGL_debug_renderer_info") or results.__contains__("UNMASKED_VENDOR_WEBGL") or results.__contains__("UNMASKED_RENDERER_WEBGL")