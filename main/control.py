import logging
import sqlite3
from typing import Dict, List, Any, Tuple
import plyvel
from pathlib import Path
import json
from analyzers.analyzer import Analyzer
from runHealth import runHealth

import argparse

import importlib

from utils import GenerateLogger, all_analyzers, get_all_symmetric_differences, load_cache, store_to_cache, run_analyzers

import sys

if __name__ == '__main__':

    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("path",  help="path of datadir directory",)
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
        analyzer_classes = args.analyzers.split(',')
        mods_classes = \
            [c.rpartition('.') for c in analyzer_classes]
        analyzer_objects : List[Analyzer] = []
        for mc in mods_classes:
            print(mc)
            if mc[0] != '':
                m = importlib.import_module(mc[0])
                analyzer_objects.append(
                    getattr(m, mc[2])(con, db, logger)
                )
            else:
                analyzer_objects.append(globals()[mc[2]](con, db, logger))

    if cached_results is not None:
        load_cache(analyzer_objects, cached_results)
    else:
        run_analyzers(analyzer_objects)

    get_all_symmetric_differences(analyzer_objects, logger)

    if cached_results is None:
        with open(path.joinpath("analysis_results.json"),"w") as results_fp:
            json.dump(store_to_cache(analyzer_objects),results_fp, indent=4)
        




    # for method in FingerprintingMethods:
    #     join : Set[Identifier] = DynamicResults[method].intersection(StaticResults[method]) #type: ignore
    #     logger.info(f"""Fingerprinting method: {method}, 
    #     in terms of pairs of (visit_id,script_url), 
    #     dynamically classified: {len(DynamicResults[method])}
    #     statically classified: {len(StaticResults[method])}
    #     intersection: {len(join)}
    #     total dynamically analyzed: {DA.total_identifiers()} 
    #     total statically analyzed: {SA.total_identifiers()} 
    #     """)
    #     join : Set[str] = DynamicResults_by_visit_id[method].intersection( StaticResults_by_visit_id[method])
    #     logger.info(f"""Fingerprinting method: {method}, 
    #     in terms of visit_id only, 
    #     dynamically classified: {len(DynamicResults_by_visit_id[method])}
    #     statically classified: {len(StaticResults_by_visit_id[method])}
    #     intersection: {len(join)}
    #     total visits: {n}
    #     """)
