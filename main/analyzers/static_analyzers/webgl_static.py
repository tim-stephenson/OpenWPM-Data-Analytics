from typing import Dict, List, Any
import sqlite3
import logging
from analyzers.static_analyzer import Static_Analyzer
from analyzers.static_analyzers.grep_utils import grepForKeywords


class WebGL_Static(Static_Analyzer):

    def __init__(self, con : sqlite3.Connection, db : Any, logger : logging.Logger) -> None:
        self.__keywords : List[str] = [".getParameter"]
        super().__init__(con,db,logger)

    def fingerprinting_type(self) -> str:
        return "WebGL"
    
    def _analyze_one(self,source_code : str) -> bool:
        results: Dict[str, bool] = grepForKeywords(self.__keywords, source_code)        
        return results[".getParameter"]