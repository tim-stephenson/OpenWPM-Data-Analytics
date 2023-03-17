from typing import  Dict, List, Tuple, Any
from sqlalchemy.engine import Engine
from sqlalchemy.sql import Select
from sqlalchemy import  MetaData, Table, select

def from_requirements(table : Table, where__clause_requirements : Dict[str,Any]) -> Select[Any] :
    stmt: Select[Any] = select(table.c["visit_id","script_url"]).where(
        *[table.c.__getitem__(k) == v for k,v in where__clause_requirements.items()])
    return stmt

def gather_buckets(analyses : Tuple[str,str], engine : Engine, table_name : str ) -> List[ Tuple[ Dict[str,bool | None], List[Tuple[str,str]] ] ]:
    buckets : List[Dict[str, bool | None]] = [
        {analyses[0] : None, analyses[1] : True},
        {analyses[0] : None, analyses[1] : False},
        {analyses[0] : None, analyses[1] : None},
        {analyses[0] : True, analyses[1] : True},
        {analyses[0] : True, analyses[1] : False},
        {analyses[0] : True, analyses[1] : None},
        {analyses[0] : False, analyses[1] : True},
        {analyses[0] : False, analyses[1] : False},
        {analyses[0] : False, analyses[1] : None},
    ]
    metadata_obj: MetaData = MetaData()
    metadata_obj.reflect(engine)
    toReturn : List[ Tuple[ Dict[str,bool | None], List[Tuple[str,str]] ] ] = []
    with engine.connect() as conn:
        for bucket in buckets:
            toReturn.append((bucket, 
            [ tuple(row) for row in conn.execute(from_requirements(metadata_obj.tables[table_name], bucket ) ).fetchall()]           
                             ))            
    return toReturn



