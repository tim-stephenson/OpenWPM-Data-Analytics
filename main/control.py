import logging
import sqlite3
from typing import List, Any
import plyvel #type: ignore
from pathlib import Path
from analyzers.analyzer import Analyzer
from utils.into_table_utils import analyzerObjects_to_dataframe, dataframe_to_table, dataframe_to_analyzerObjects,table_to_dataframe, TABLE_NAME, table_exists
from utils.runHealth import runHealth
from utils.clustering import clusters

import argparse
import pandas

from utils.utils import GenerateLogger
from utils.analyzers_utils import all_analyzers, analyzers_from_class_names, run_analyzers, get_all_symmetric_differences

if __name__ == '__main__':

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("path", type=str , help="path of datadir directory", action="store")
    parser.add_argument('--leveldb', type=str, action='store',
        help='Name of LevelDB created by OpenWPM', default='leveldb')
    parser.add_argument("--from_cache", help="use analysis data from previous run", action="store_true")
    parser.add_argument('--analyzers', type=str, action='store',
        help='Comma-separated list of names of analyzer classes to use', 
        default=None)
    args: argparse.Namespace = parser.parse_args()

    path : Path = Path(args.path)
    logger: logging.Logger = GenerateLogger(path.joinpath("analysis.log") )
    con : sqlite3.Connection = sqlite3.connect( str(path.joinpath("crawl-data.sqlite")) )
    db : Any = plyvel.DB( str(path.joinpath(args.leveldb)) ) # type: ignore

    load_from_cache : bool = args.__getattribute__("from_cache")
    if load_from_cache and not table_exists(TABLE_NAME,con):
        load_from_cache = False
        logger.warning("Program was run with '--from-cache' yet no cache exits. Program is ignoring --from-cache flag.")

    n,f = runHealth(con)
    logger.info(f"total visits: {n}, failed/incomplete visits: {f}. Success percentage: {round(100* (1 - f/n)) }%")

    if args.analyzers is None:
        analyzer_objects: List[Analyzer] = all_analyzers(con,db,logger)
    else:
        analyzer_objects: List[Analyzer] = analyzers_from_class_names(str(args.analyzers).split(','), con,db,logger)

    if load_from_cache:
        df : pandas.DataFrame =  table_to_dataframe(con)
        dataframe_to_analyzerObjects(analyzer_objects,df)
    else:
        run_analyzers(analyzer_objects)
        df : pandas.DataFrame = analyzerObjects_to_dataframe(analyzer_objects)
        dataframe_to_table(df,con)

    get_all_symmetric_differences(analyzer_objects, logger)
    clusters(df,logger)

    
