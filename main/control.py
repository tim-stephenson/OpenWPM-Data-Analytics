import logging
import sqlite3
from typing import Dict, List, Any, Tuple
import plyvel #type: ignore
from pathlib import Path
import json
from analyzers.analyzer import Analyzer
from runHealth import runHealth

import argparse


from utils import GenerateLogger, all_analyzers, analyzers_from_class_names, get_all_symmetric_differences, load_cache, store_to_cache, run_analyzers

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
    cached_results : None | Dict[str, List[Tuple[str, str]]] = None
    if args.__getattribute__("from_cache"):
        try:
            with open(path.joinpath("analysis_results.json"),"r") as results_fp:
                cached_results = { k : [tuple(pair) for pair in v] for k,v in dict(json.load(results_fp)).items() }
        except FileNotFoundError:
            logger.warning("Program was run with '--from-cache' yet no cache exits. Program is ignoring --from-cache flag.")
    
    con : sqlite3.Connection = sqlite3.connect( str(path.joinpath("crawl-data.sqlite")) )
    db : Any = plyvel.DB( str(path.joinpath(args.leveldb)) ) # type: ignore

    n,f = runHealth(con)
    logger.info(f"total visits: {n}, failed/incomplete visits: {f}. Success percentage: {round(100* (1 - f/n)) }%")

    if args.analyzers is None:
        analyzer_objects: List[Analyzer] = all_analyzers(con,db,logger)
    else:
        analyzer_objects: List[Analyzer] = analyzers_from_class_names(str(args.analyzers).split(','), con,db,logger)

    if cached_results is not None:
        load_cache(analyzer_objects, cached_results)
    else:
        run_analyzers(analyzer_objects)

    get_all_symmetric_differences(analyzer_objects, logger)

    if cached_results is None:
        with open(path.joinpath("analysis_results.json"),"w") as results_fp:
            json.dump(store_to_cache(analyzer_objects),results_fp, indent=4)

    
