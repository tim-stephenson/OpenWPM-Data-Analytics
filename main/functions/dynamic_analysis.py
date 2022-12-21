

import ast
import logging
import math
import sqlite3
from typing import Dict, List, Set, Tuple, Union
import pandas as pd

from main.functions.analysis import Analysis, Identifier

# (visit_id, script_url)
# Identifier = Tuple[str,str]

class DynamicAnalysis(Analysis):
    """
    """

    def __init__(self, con : sqlite3.Connection, db : any, logger : logging.Logger) -> None:
        self.con = con
        self.logger = logger

    def run(self) -> Dict[str, List[Identifier] ]:
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
        results : Dict[str, List[Identifier] ] = {
            "Canvas" : []
        }
        previous : Union[ Identifier, None]  = None
        lst: List[any] = []
        i : int = 0
        cols : List[str] = [column[0] for column in ordered.description]
        for row in ordered:
            if(i % 10000 == 0):
                 self.logger.info(f"Done: {i} out of {n}")
            i += 1

            id : Identifier = (row["visit_id"], row["script_url"] )
            if(previous == None):
                previous = id
            if( previous != id ):
                fingerprinting_methods = self._Analyze( pd.DataFrame(lst, columns=cols) )
                for method in fingerprinting_methods:
                    results[method].append(id)
                lst = []
                previous = id
            lst.append(row)
        return results



    def _Analyze(self,df : pd.DataFrame ) -> List[str]:
        lst : List[str] = []
        if self._Canvas(df):
            lst.append("Canvas")
        return lst
       


    def _Canvas(self,df :  pd.DataFrame) -> bool:
        # condition 1:
        heightORwidthTooSmall : bool = False
        # condition 2:
        colors : Set[str] = set()
        characters : Set[str] = set()
        # condition 3:
        ProductiveCalls : bool = False
        #Condition 4:
        Extraction : bool = False
        for row in df.itertuples():
            try:
                match row.symbol:
                    case 'HTMLCanvasElement.height':
                        if row.operation == 'set' and row.value and float(row.value) < 16:
                            heightORwidthTooSmall = True
                    case 'HTMLCanvasElement.width':
                        if row.operation == 'set' and row.value and float(row.value) < 16:
                            heightORwidthTooSmall = True
                    case 'CanvasRenderingContext2D.fillText':
                        args = ast.literal_eval(row.arguments)
                        for char in args[0]:
                            characters.add(char)
                    case 'CanvasRenderingContext2D.fillStyle':
                        if row.operation == 'set' and row.value:
                            colors.add(row.value)
                    case 'HTMLCanvasElement.toDataURL':
                        Extraction = True
                    case 'CanvasRenderingContext2D.getImageData':
                        args = ast.literal_eval(row.arguments)
                        if abs( args[2] ) >= 16 and abs( args[3] ) >= 16:
                            Extraction = True
                    case 'HTMLCanvasElement.addEventListener':
                        ProductiveCalls = True
                    case 'CanvasRenderingContext2D.save':
                        ProductiveCalls = True
                    case 'CanvasRenderingContext2D.restore':
                        ProductiveCalls = True
            except Exception as e:
                self.logger.exception(f"Found Exception {e}")

        #       condition 1                    condition 2                                   condition 3            condition 4
        return (not heightORwidthTooSmall) and ( len(colors) > 2 or len(characters) > 10) and (not ProductiveCalls) and Extraction