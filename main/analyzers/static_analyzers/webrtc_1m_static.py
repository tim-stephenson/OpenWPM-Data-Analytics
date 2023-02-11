from typing import Dict, List, Any
import sqlite3
import logging
from analyzers.static_analyzer import Static_Analyzer
from analyzers.static_analyzers.grep_utils import grepForKeywords


class WebRTC_1M_Static(Static_Analyzer):


    def __init__(self, con : sqlite3.Connection, db : Any, logger : logging.Logger) -> None:
        self.__keywords : List[str] = [".createDataChannel",".createOffer",".onicecandidate"]
        super().__init__(con,db,logger)
    

    def fingerprinting_type(self) -> str:
        return "WebRTC"
    
    def _analyze_one(self,source_code : str) -> bool:
        results: Dict[str, bool] = grepForKeywords(self.__keywords, source_code) 
        return results[".createDataChannel"] and results[".createOffer"] and results[".onicecandidate"]