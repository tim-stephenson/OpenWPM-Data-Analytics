import logging
from sqlalchemy import create_engine, URL
from sqlalchemy.engine import Engine
from typing import List, Any
import plyvel #type: ignore
from pathlib import Path
from analyzers.analyzer import Analyzer
from utils.into_table_utils import analyzerObjects_to_dataframe, dataframe_to_table, PROTECTED_TABLE_NAMES
from utils.runHealth import runHealth

import argparse
import pandas
import sys

from utils.utils import GenerateLogger
from utils.analyzers_utils import all_analyzers, analyzers_from_class_names, run_analyzers

if __name__ == '__main__':

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("path", type=str , action="store",
        help="path of datadir directory")
    parser.add_argument('--leveldb', type=str, action='store',
        help='Name of LevelDB created by OpenWPM', default='leveldb')
    parser.add_argument('--analyzers', type=str, action='store',
        help='Comma-separated list of names of analyzer classes to use', default="")
    parser.add_argument("--table_name", type=str, action="store",
        help="Table Name to store the analysis results, default = 'analysis_results'", default="analysis_results")
    args: argparse.Namespace = parser.parse_args()

    datadir_path : Path = Path(args.path).resolve(strict=True)
    logger: logging.Logger = GenerateLogger(datadir_path.joinpath("analysis.log") )
    database_url : URL = URL.create(drivername = "sqlite", database = str(datadir_path.joinpath("crawl-data.sqlite")) )
    engine : Engine = create_engine(database_url)
    db : Any = plyvel.DB( str(path.joinpath(args.leveldb)) ) # type: ignore

    table_name : str = args.table_name
    if table_name in PROTECTED_TABLE_NAMES:
        logger.error(f"""Cannot use a table name used by the OpenWPM output data.
Your table name: {table_name}
The table names used by OpenWPM:\n{PROTECTED_TABLE_NAMES}""")
        sys.exit(1)

    n,s = runHealth(engine)
    logger.info(f"total visits: {n}, 'functional' visits: {s}. Success percentage: {round(100* (s/n)) }%")

    if args.analyzers == "":
        analyzer_objects: List[Analyzer] = all_analyzers(engine,db,logger)
    else:
        analyzer_objects: List[Analyzer] = analyzers_from_class_names(str(args.analyzers).split(','), engine,db,logger)


    run_analyzers(analyzer_objects)
    df : pandas.DataFrame = analyzerObjects_to_dataframe(analyzer_objects)
    dataframe_to_table(df,engine,table_name)


    
