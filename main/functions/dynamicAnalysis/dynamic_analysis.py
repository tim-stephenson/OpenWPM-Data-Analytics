import logging
import sqlite3
from typing import Dict, List, Set, Union, Callable
import pandas as pd

from main.functions.analysis import Analysis, Identifier
from main.functions.dynamicAnalysis.canvas import Canvas


methods : Dict[str, Callable[[pd.DataFrame, logging.Logger], bool]] = {
    "Canvas" : Canvas
}

class DynamicAnalysis(Analysis):

    def __init__(self, con : sqlite3.Connection, db : any, logger : logging.Logger) -> None:
        self.con = con
        self.logger = logger


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
        numEntries : sqlite3.Cursor = self.con.cursor().execute(
            """SELECT COUNT(visit_id)
            FROM javascript"""
            )
        n : int = numEntries.fetchone()[0]
        ordered : sqlite3.Cursor = self.con.cursor().execute(
            """SELECT * 
            FROM javascript 
            ORDER BY visit_id, script_url"""
            )
        ordered.row_factory = sqlite3.Row
        cols : List[str] = [column[0] for column in ordered.description]


        results : Dict[str, Set[Identifier] ] = { k : set() for k in methods }
        previous : Union[ Identifier, None]  = None
        lst: List[any] = []
        for row in ordered:
            id : Identifier = (row["visit_id"], row["script_url"] )
            if(previous == None):
                previous = id
            if( previous != id ):
                fingerprinting_methods = self._Analyze( pd.DataFrame(lst, columns=cols) )
                for fingerprintingMethod in fingerprinting_methods:
                    self.logger.info(f"{id} using {fingerprintingMethod}")
                    results[fingerprintingMethod].add(id)
                lst = []
                previous = id
            lst.append(row)
        return results



    def _Analyze(self,df : pd.DataFrame ) -> List[str]:
        lst : List[str] = []
        for k, v in methods.items():
            if(v(df, self.logger)):
                lst.append(k)
        return lst
       


