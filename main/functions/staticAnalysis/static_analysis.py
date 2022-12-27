
import functools
import logging
import sqlite3
from typing import Callable, Dict, List, Set

from main.functions.analysis import Analysis, Identifier
from main.functions.staticAnalysis.canvas import Canvas
from main.functions.staticAnalysis.webrtc import WebRTC
from main.functions.staticAnalysis.canvas_font import CanvasFont


methods : Dict[str, Callable[[str, logging.Logger], bool] ] = {
    "Canvas" : Canvas,
    "WebRTC" : WebRTC,
    "CanvasFont" : CanvasFont
}

class StaticAnalysis(Analysis):

    def __init__(self, con : sqlite3.Connection, db : any, logger : logging.Logger) -> None:
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
    
    def run(self) -> Dict[str, Set[Identifier] ]:
        responses : sqlite3.Cursor = self.con.cursor().execute(
            """SELECT id, visit_id, headers, url, content_hash
            FROM http_responses 
            WHERE content_hash <> "" """
            )
        responses.row_factory = sqlite3.Row

        results : Dict[str, Set[Identifier] ] = { k : set() for k in methods }
        for row in responses:
            script_analyze_results : List[str] = self._Analyze(bytes( row["content_hash"], encoding="ascii" ))
            id : Identifier = (row["visit_id"], row["url"] )
            for fingerprintingMethod in script_analyze_results:
                self.logger.info(f"{id} using {fingerprintingMethod}")
                results[fingerprintingMethod].add(id)
        return results

    @functools.cache
    def _Analyze(self,content_hash : bytes) -> List[str]:
        code : str = str( self.db.get(content_hash) ,encoding="utf-8", errors='ignore')
        toReturn : List[str] = []
        for k, v in methods.items():
            if(v(code,self.logger)):
                toReturn.append(k)
        return toReturn