import sqlite3
from typing import Tuple

def runHealth(con : sqlite3.Connection) -> Tuple[int,int]:
    total = con.cursor().execute("SELECT COUNT(visit_id) FROM site_visits")
    failures = con.cursor().execute("SELECT COUNT(DISTINCT visit_id) FROM incomplete_visits")
    return( total.fetchone()[0], failures.fetchone()[0] )

