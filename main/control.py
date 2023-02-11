# control code
import logging
import sqlite3
from typing import Dict, List, Any, Tuple
import plyvel # type: ignore
from pathlib import Path
import json
from runHealth import runHealth

import argparse

from utils import GenerateLogger, run_all_analyzers

if __name__ == '__main__':
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of datadir directory")
    args: argparse.Namespace = parser.parse_args()
    path : Path = Path(args.path)

    logger: logging.Logger = GenerateLogger(path.joinpath("analysis2.log") )

    con : sqlite3.Connection = sqlite3.connect( str(path.joinpath("crawl-data.sqlite")) )
    db : Any = plyvel.DB( str(path.joinpath("leveldb")) ) # type: ignore

    n,f = runHealth(con)
    logger.info(f"total visits: {n}, failed/incomplete visits: {f}. Success percentage: {round(100* (1 - f/n)) }%")

    results: Dict[str, List[Tuple[str, str]]] = run_all_analyzers(con,db,logger)

    with open(path.joinpath("analysis_results.json"),"w") as fileObj:
        json.dump(results,fileObj, indent=4)

