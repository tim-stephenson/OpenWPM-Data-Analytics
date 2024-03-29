import argparse
import logging
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Tuple
import plyvel #type: ignore
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, URL
from utils.dump_source_code import dump_from_identifier_list
from utils.utils import GenerateLogger
import datetime
import subprocess
import json

from utils.into_table_utils import column_exists, table_exists, PROTECTED_TABLE_NAMES
from utils.gather_buckets import gather_buckets



if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("path", type=str , action="store",
        help="path of datadir directory")
    parser.add_argument("--table_name", type=str, action="store",
        help="Table Name of the analysis results, default = 'analysis_results'", default="analysis_results")
    parser.add_argument('--leveldb', type=str, action='store',
        help='Name of LevelDB created by OpenWPM', default='leveldb')
    parser.add_argument('--dump_source_code', action='store_true',
        help="""create folders with the source code (prettified) for each portion of the venn diagram between the analyzers' results,
        so long at least one of the analyzers classified the (visit_id,script_url) pair as preforming fingerprinting""", default=False)
    parser.add_argument("analyzers_names", nargs="+",
        help="List of analyzers_names to compare. At least one must provided.")
    
    args: argparse.Namespace = parser.parse_args()

    datadir_path : Path = Path(args.path).resolve(strict=True)
    logger: logging.Logger = GenerateLogger(datadir_path.joinpath("view_results.log") )
    database_url : URL = URL.create(drivername = "sqlite", database = str(datadir_path.joinpath("crawl-data.sqlite")) )
    engine : Engine = create_engine(database_url)
    db : Any = plyvel.DB( str(datadir_path.joinpath(args.leveldb)) ) # type: ignore

    table_name : str = args.table_name
    analyses : List[str] = args.analyzers_names

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


    
    buckets: List[ Tuple[Dict[str, bool | None], List[Tuple[str, str]]]] = gather_buckets(analyses, engine, table_name)
        

    for bucket, value in buckets:
        logger.info(f""" {json.dumps(bucket, separators=(',', ':'))}     :    {len(value)} """)


    if args.dump_source_code:
        dump_source_code_path: Path = datadir_path.joinpath(f"temp-{datetime.datetime.now().replace(microsecond=0).isoformat()}")
        dump_source_code_path.mkdir()
        for bucket, value in buckets:
            if any( bucket.values() ):
                dir_path: Path = dump_source_code_path.joinpath(json.dumps(bucket, separators=(',', ':')))
                dir_path.mkdir()
                dump_from_identifier_list(value,engine,db,dir_path)


        node_script_path: Path = Path(__file__).parent.parent.joinpath("node","run.sh").resolve()
        process: subprocess.Popen[str] = subprocess.Popen( [
            "bash","-i",str(node_script_path),"npm","run","prettier","--","--ignore-unknown","--no-config","--write",dump_source_code_path
            ],text=True, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        for line in iter(process.stdout.readline, b""): #type: ignore
            if line == "":
                if process.poll() != None:
                    break
                time.sleep(1)
            else:
                logger.info(line)

    





