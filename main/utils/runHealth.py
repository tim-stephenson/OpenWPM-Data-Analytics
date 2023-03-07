from typing import Tuple
from sqlalchemy.engine import Engine
from sqlalchemy import text, CursorResult

def runHealth(engine : Engine) -> Tuple[int,int]:
    with engine.connect() as conn:
        total: CursorResult[Tuple[int]] = conn.execute(text("SELECT COUNT(visit_id) FROM site_visits"))
        failures: CursorResult[Tuple[int]] = conn.execute(text("SELECT COUNT(DISTINCT visit_id) FROM incomplete_visits"))
        return( total.__next__().tuple()[0], failures.__next__()[0] )

