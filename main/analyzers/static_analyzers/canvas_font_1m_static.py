import logging
import sqlite3
from typing import Dict, Any, List
from analyzers.static_analyzer import Static_Analyzer
from analyzers.static_analyzers.grep_utils import grepForKeywords


class Canvas_Font_1M_Static(Static_Analyzer):

    def __init__(self, con : sqlite3.Connection, db : Any, logger : logging.Logger) -> None:
        self.__keywords : List[str] = [".measureText", ".font"]
        super().__init__(con,db,logger)

    def fingerprinting_type(self) -> str:
        return "Canvas Font"
    
    def _analyze_one(self,source_code : str) -> bool:
        results: Dict[str, bool] = grepForKeywords(self.__keywords, source_code)
        return results[".measureText"] and results[".font"]