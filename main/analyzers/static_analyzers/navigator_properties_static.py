from typing import List, Any, Set
import sqlite3
import logging
from analyzers.static_analyzer import Static_Analyzer
from utils.grep_utils import grepForKeywords


class Navigator_Properties_Static(Static_Analyzer):


    def __init__(self, con : sqlite3.Connection, db : Any, logger : logging.Logger) -> None:
        self.__keywords : List[str] = [".estimate",".enumerateDevices", 
                                         ".hardwareConcurrency",".language",".maxTouchPoints"]
        super().__init__(con,db,logger)

    def fingerprinting_type(self) -> str:
        return "Navigator Properties"
    
    def _analyze_one(self,source_code : str) -> bool:
        results: Set[str] = grepForKeywords(self.__keywords, source_code) 

        return len(results) >= len(self.__keywords)-2