
import functools
import logging
import sqlite3
from typing import Callable, Dict, List, Set, Any

from functions_old.analysis import Analysis, Identifier
from functions_old.staticAnalysis.canvas import Canvas
from functions_old.staticAnalysis.webrtc import WebRTC
from functions_old.staticAnalysis.canvas_font import CanvasFont
from functions_old.staticAnalysis.webgl import WebGL


methods : Dict[str, Callable[[str, logging.Logger], bool] ] = {
    "Canvas" : Canvas,
    "WebRTC" : WebRTC,
    "CanvasFont" : CanvasFont,
    "WebGL" : WebGL
}

class StaticAnalysis(Analysis):

    def __init__(self, con : sqlite3.Connection, db : Any, logger : logging.Logger) -> None:
        self.con = con
        self.db = db
        self.logger = logger

    def total_identifiers(self) -> int:
        query_response = sqlite3.Cursor = self.con.cursor().execute("""
            WITH a AS (
            SELECT visit_id,url
            FROM http_responses
            WHERE content_hash <> ""
            GROUP BY visit_id,url
            )
            SELECT COUNT(*)
            FROM a
        """)
        n : int = query_response.fetchone()[0]
        return n
    
    def run(self, dry_run : bool = False) -> Dict[str, Set[Identifier] ]:
        results : Dict[str, Set[Identifier] ] = { k : set() for k in methods }
        if dry_run:
            return results
        responses : sqlite3.Cursor = self.con.cursor().execute("""
            SELECT id, visit_id, headers, url, content_hash
            FROM http_responses 
            WHERE content_hash <> "" 
        """)
        responses.row_factory = sqlite3.Row #type: ignore
        for row in responses:
            script_analyze_results : List[str] = self.__Analyze(bytes( row["content_hash"], encoding="ascii" ))
            id : Identifier = (row["visit_id"], row["url"] )
            for fingerprintingMethod in script_analyze_results:
                self.logger.info(f"{id} using {fingerprintingMethod}")
                results[fingerprintingMethod].add(id)
        return results

    @functools.cache
    def __Analyze(self,content_hash : bytes) -> List[str]:
        code : str = str( self.db.get(content_hash) ,encoding="utf-8", errors='ignore')
        toReturn : List[str] = []
        for k, v in methods.items():
            if(v(code,self.logger)):
                toReturn.append(k)
        return toReturn