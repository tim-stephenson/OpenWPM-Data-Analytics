from pathlib import Path
from sqlalchemy.engine import Engine
from sqlalchemy import CursorResult, text
from typing import Any, List, Tuple, Set


def dump_from_content_hash(content_hash : bytes, db : Any, dir : Path) -> None:
    print(str(content_hash,encoding="ascii") + ".js" )
    with open(dir.joinpath( str(content_hash,encoding="ascii") + ".js" ),"wb") as fp:
        fp.write(db.get(content_hash))



def dump_from_identifier_list(lst : List[Tuple[str,str]], engine : Engine, db : Any, dir : Path) -> None:
    identifier_set: frozenset[Tuple[str, str]] = frozenset(lst)
    print(lst)
    with engine.connect() as conn:
        query_response : CursorResult[Any] = conn.execute(text("""
            SELECT DISTINCT visit_id, url, content_hash
            FROM http_responses
            WHERE content_hash <> ""
        """))
    content_hashes : Set[bytes] = set()
    for row in query_response.mappings():
        if (row["visit_id"],row["url"]) in identifier_set:
            content_hashes.add( bytes(row["content_hash"], encoding="ascii") )
    for content_hash in content_hashes:
        dump_from_content_hash(content_hash,db, dir)

