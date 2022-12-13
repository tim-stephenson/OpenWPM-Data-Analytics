
import ast
import math
import sqlite3
import subprocess
from typing import Dict, List, Set, Tuple, Union
import pandas as pd

# (visit_id, script_url)
Identifier = Tuple[str,str]

# returns a dict[ fingerprinting method ] = [ (visit_id,script_url), ... ]
def Static(con : sqlite3.Connection, db : any) -> Dict[str, List[Identifier] ]:
    # build
    subprocess.run(["sh", "node/run.sh", "npm run build"])

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
        if(i % 10000 == 0):
            print(f"Done: {i} out of {n}")
        i += 1

        code : str = db.get( bytes( row["content_hash"], encoding="ascii" ) )
        # completedProcess : subprocess.CompletedProcess = subprocess.run(["sh", f"node/run.sh \"npm run execute \"{code}\"\""])
        code : str = "1+1"
        completedProcess : subprocess.CompletedProcess = subprocess.run(["sh", "node/run.sh", f"npm run execute \"{code}\""])
        id : Identifier = (row["visit_id"], row["url"] )
        if completedProcess.returncode == 1:
            results["Canvas"].append(id)
            print(f"Found: {id}")
    return results
