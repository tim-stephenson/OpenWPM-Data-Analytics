import logging
import sqlite3
from typing import Dict, List, Set, Union

import pandas as pd

from main.functions.analysis import Analysis, Identifier
from main.functions.dynamicAnalysis.canvas import Canvas
from main.functions.dynamicAnalysis.webrtc import WebRTC
from main.functions.dynamicAnalysis.canvas_font import CanvasFont
from main.functions.dynamicAnalysis.dynamic_analysis_ABC import DynamicAnalysisABC




class DynamicAnalysis(Analysis):

    def __init__(self, con : sqlite3.Connection, db : any, logger : logging.Logger) -> None:
        self.con = con
        self.logger = logger
        self.analyzers : List[DynamicAnalysisABC] = [Canvas(self.logger), WebRTC(self.logger), CanvasFont(self.logger)]


    def total_identifiers(self) -> int:
        query_response = sqlite3.Cursor = self.con.cursor().execute("""
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

    def run(self) -> Dict[str, Set[Identifier] ]:
        ordered : sqlite3.Cursor = self.con.cursor().execute(
            """SELECT * 
            FROM javascript 
            ORDER BY visit_id, script_url"""
            )
        ordered.row_factory = sqlite3.Row

        results : Dict[str, Set[Identifier] ] = { str(analyzer) : set() for analyzer in self.analyzers }
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
            for analyzer in self.analyzers:
                analyzer.read_row(row)
        return results
    
       


