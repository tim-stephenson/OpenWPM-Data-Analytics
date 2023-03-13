from typing import Tuple
from sqlalchemy.engine import Engine
from sqlalchemy import text, CursorResult

def runHealth(engine : Engine) -> Tuple[int,int]:
    with engine.connect() as conn:
        total: CursorResult[Tuple[int]] = conn.execute(text("SELECT COUNT(DISTINCT visit_id) FROM site_visits"))
        successes: CursorResult[Tuple[int]] = conn.execute(text("""
            SELECT COUNT(DISTINCT visit_id) 
            FROM http_responses WHERE 
            response_status LIKE "2%"
        """))
        return( total.__next__().tuple()[0], successes.__next__()[0] )

