import json
import logging
import sqlite3
from typing import Any, Dict, List, Set, Union

from functions_old.analysis import Analysis, Identifier
from functions_old.dynamicAnalysis.canvas import Canvas
from functions_old.dynamicAnalysis.webrtc import WebRTC
from functions_old.dynamicAnalysis.canvas_font import CanvasFont
from functions_old.dynamicAnalysis.dynamic_analysis_ABC import DynamicAnalysisABC
from functions_old.dynamicAnalysis.webgl import WebGL




class DynamicAnalysis(Analysis):

    def __init__(self, con : sqlite3.Connection, db : Any, logger : logging.Logger) -> None:
        self.con = con
        self.logger = logger
        self.analyzers : List[DynamicAnalysisABC] = [Canvas(self.logger), WebRTC(self.logger), CanvasFont(self.logger), WebGL(self.logger)]

    def total_identifiers(self) -> int:
        query_response : sqlite3.Cursor = self.con.cursor().execute("""
            WITH a AS (
            SELECT visit_id,script_url
            FROM javascript
            GROUP BY visit_id,script_url
            )
            SELECT COUNT(*)
            FROM a
        """)
        n : int = query_response.fetchone()[0]
        return n

    def run(self, dry_run : bool = False) -> Dict[str, Set[Identifier] ]:
        results : Dict[str, Set[Identifier] ] = { str(analyzer) : set() for analyzer in self.analyzers }
        if dry_run:
            return results
        ordered : sqlite3.Cursor = self.con.cursor().execute(
            """SELECT * 
            FROM javascript 
            ORDER BY visit_id, script_url"""
            )
            
        ordered.row_factory = sqlite3.Row  # type: ignore

        previous : Union[ Identifier, None]  = None
        for row in ordered:
            
            id : Identifier = (row["visit_id"], row["script_url"] )
            if(previous == None):
                previous = id
            if( previous != id ):
                for analyzer in self.analyzers:
                    if analyzer.classify():
                        self.logger.info(f"{previous} using {str(analyzer)}")
                        results[str(analyzer)].add(previous)
                    analyzer.reset()
                previous = id
            parsedArguments = self.__parseArguments(row["arguments"])
            for analyzer in self.analyzers:
                analyzer.read_row(row, parsedArguments)
        return results

    def __parseArguments(self,arguments : None | str) -> Any | None:
        if arguments is None:
            return None
        return json.loads(arguments)
    
       

