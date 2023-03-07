import argparse
# import datetime
import logging
from pathlib import Path
import sys
from typing import Any, Dict, List, Tuple
import plyvel #type: ignore
from sqlalchemy.engine import Engine
from sqlalchemy.sql import Select
from sqlalchemy import  Table, MetaData, select, create_engine
from utils.utils import GenerateLogger

from utils.into_table_utils import column_exists, table_exists, PROTECTED_TABLE_NAMES

def from_requirements(table : Table, where__clause_requirements : Dict[str,Any]) -> Select[Any] :
    stmt: Select[Any] = select(table).where(
        *[table.c.__getitem__(k) == v for k,v in where__clause_requirements.items()])
    return stmt



if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("path", type=str , action="store",
        help="path of datadir directory")
    parser.add_argument("--table_name", type=str, action="store",
        help="Table Name of the analysis results, default = 'analysis_results'", default="analysis_results")
    parser.add_argument('--leveldb', type=str, action='store',
        help='Name of LevelDB created by OpenWPM', default='leveldb')
    parser.add_argument("analysis_name_1", type=str, action="store",
        help="Analysis Name to compare against")
    parser.add_argument("analysis_name_2", type=str, action="store",
        help="Analysis Name to compare against")
    
    args: argparse.Namespace = parser.parse_args()


    path : Path = Path(args.path).resolve(strict=True)
    logger: logging.Logger = GenerateLogger(path.joinpath("analysis.log") )
    engine : Engine = create_engine(f"""sqlite:///{path.joinpath("crawl-data.sqlite")}""")
    db : Any = plyvel.DB( str(path.joinpath(args.leveldb)) ) #type: ignore
    table_name : str = args.table_name
    analyses : Tuple[str,str] = (args.analysis_name_1,args.analysis_name_2)

    if table_name in PROTECTED_TABLE_NAMES:
        logger.error(f"""Cannot use a table name used by the OpenWPM output data.
Your table name: {table_name}
The table names used by OpenWPM:\n{PROTECTED_TABLE_NAMES}""")
        sys.exit(1)
    if not table_exists( table_name, engine):
        logger.error(f"Table name : {table_name} does not exist in the sql database")
        sys.exit(1)
    for analysis_name in analyses:
        if not column_exists(table_name, analysis_name,engine):
            logger.error(f"analysis name : {analysis_name} is not present in the {table_name} table")
            sys.exit(1)



    metadata_obj: MetaData = MetaData()
    with engine.connect() as conn:

        both: List[Tuple[str,str]] = conn.execute(from_requirements(metadata_obj.tables[table_name], 
            {analyses[0] : 1, analyses[1] : 1} ) ).fetchall()  # type: ignore
        
        just_1: List[Tuple[str,str]] = conn.execute(from_requirements(metadata_obj.tables[table_name], 
            {analyses[0] : 1, analyses[1] : 0} ) ).fetchall()  # type: ignore
        
        just_2: List[Tuple[str,str]] = conn.execute(from_requirements(metadata_obj.tables[table_name], 
            {analyses[0] : 0, analyses[1] : 1} ) ).fetchall()  # type: ignore
        
        neither: List[Tuple[str,str]] = conn.execute(from_requirements(metadata_obj.tables[table_name], 
            {analyses[0] : 0, analyses[1] : 0} ) ).fetchall()  # type: ignore
        


    logger.info(f"""
    {len(both)}
    {len(just_1)}
    {len(just_2)}
    {len(neither)}
    """)
    # dump_source_code_path: Path = path.joinpath(f"temp-{datetime.datetime.now().replace(microsecond=0).isoformat()}")
    # dump_source_code_path.mkdir()



