
import ast
import math
import re
import sqlite3
import subprocess
from typing import Dict, List, Set, Tuple, Union
import pandas as pd
import jsbeautifier

# (visit_id, script_url)
Identifier = Tuple[str,str]

# returns a dict[ fingerprinting method ] = [ (visit_id,script_url), ... ]
def Static(con : sqlite3.Connection, db : any) -> Dict[str, List[Identifier] ]:
    numEntries : sqlite3.Cursor = con.cursor().execute(
        """SELECT COUNT(visit_id)
        FROM http_responses 
        WHERE content_hash <> "" """
        )
    n : int = numEntries.fetchone()[0]
    responses : sqlite3.Cursor = con.cursor().execute(
        """SELECT id, visit_id, headers, url, content_hash
        FROM http_responses 
        WHERE content_hash <> "" """
        )
    responses.row_factory = sqlite3.Row
    results : Dict[str, List[Identifier] ] = {
        "Canvas" : []
    }
    i : int = 0
    for row in responses:
        if(i % 100 == 0):
            print(f"Done: {i} out of {n}")
        i += 1

        code : str = str( db.get( bytes( row["content_hash"], encoding="ascii" ) ),encoding="UTF-8")
        id : Identifier = (row["visit_id"], row["url"] )
        Analyze(code, results, id)
    return results

def Analyze(code : str, results : Dict[str, List[Identifier] ], id : Identifier ) -> None:
    code = jsbeautifier.beautify(code)
    if Canvas(code):
        results["Canvas"].append(id)
        print(f"Found: {id}")

def Canvas(code : str):
    try:
        # m : re.Match = re.search("toDataURL",code)
        # print(m)
        # if m.lastindex != None:
        #   for g in range(m.lastindex + 1):
        #       print( m.string[(m.start(g)-10):(m.end(g) + 10)] )
        for m in re.finditer("toDataURL",code):
            print("-"*30)
            print( m.string[(m.start(0)-10):(m.end(0) + 10)] )
            print("-"*30)
    except Exception as e:
        print(f"Found Exception {e}")

    return True


"""
    # build
    subprocess.run(["sh", "node/run.sh", "npm run build"])
    completedProcess : subprocess.CompletedProcess = subprocess.run(["sh", "node/run.sh", f"npm run execute \"{code}\""])

"""