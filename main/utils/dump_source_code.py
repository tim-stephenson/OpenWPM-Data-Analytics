from pathlib import Path
from sqlalchemy.engine import Engine
from typing import List, Tuple


def dump_from_content_hash(content_hash : bytes, dir : Path) -> None:
    pass


def dump_from_identifier_list(lst : List[Tuple[str,str]], engine : Engine, dir : Path) -> None:
    # for visit_id, script_url in lst:
    #     query_response: sqlite3.Cursor = con.execute("""
    #         SELECT DISTINCT content_hash
    #         FROM http_responses
    #         WHERE visit_id = ? AND script_url = ?
    #     """,[visit_id,script_url])
    pass

