

import ast
import sqlite3
from typing import Dict, List, Tuple, Union
import pandas as pd

# (visit_id, script_url)
Identifier = Tuple[str,str]

# returns a dict[ fingerprinting method ] = [ (visit_id,script_url), ... ]
def Dynamic(con : sqlite3.Connection) -> Dict[str, List[Identifier] ]:
    numEntries : sqlite3.Cursor = con.cursor().execute(
        """SELECT COUNT(visit_id)
        FROM javascript"""
        )
    n : int = numEntries.fetchone()[0]
    ordered : sqlite3.Cursor = con.cursor().execute(
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
            print(f"Done: {i} out of {n}")
        i += 1

        if(previous == None):
            previous = (row["visit_id"], row["script_url"] )
        if( previous != (row["visit_id"], row["script_url"]) ):
            Analyze( pd.DataFrame(lst, columns=cols), results, previous )
            lst = []
            previous = (row["visit_id"], row["script_url"]) 
        lst.append(row)
    return results


def Analyze(df : pd.DataFrame, results : Dict[str, List[Identifier] ], id : Identifier ) -> None:
    if Canvas(df):
        results["Canvas"].append(id)
        print(f"Found: {id}")
       


def Canvas(df :  pd.DataFrame) -> bool:
    heightRec = False
    widthRec = False
    colors = set()
    characters = set()
    Extraction = False
    for row in df.itertuples():
        try:
            match row.symbol:
                case 'HTMLCanvasElement.height':
                    if row.operation == 'set' and row.value and float(row.value) >= 16:
                        heightRec = True
                case 'HTMLCanvasElement.width':
                    if row.operation == 'set' and row.value and float(row.value) >= 16:
                        widthRec = True
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
                    Extraction = True
        except Exception as e:
            print(f"Found Exception {e}")
    return heightRec and widthRec and ( len(colors) > 2 or len(characters) > 10) and Extraction