import logging
import sqlite3
from typing import Set, Any, List
from analyzers.static_analyzer import Static_Analyzer
from utils.grep_utils import grepForKeywords


class Canvas_Font_1M_Static(Static_Analyzer):

    def __init__(self, con : sqlite3.Connection, db : Any, logger : logging.Logger) -> None:
        self.__keywords : List[str] = [".measureText", ".font"]
        super().__init__(con,db,logger)

    def fingerprinting_type(self) -> str:
        return "Canvas Font"
    
    def _analyze_one(self,source_code : str) -> bool:
        results: Set[str] = grepForKeywords(self.__keywords, source_code)
        return results.__contains__(".measureText") and results.__contains__(".font")