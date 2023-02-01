# control code
import logging
import sqlite3
from typing import Dict, List, Set, Any
import plyvel
from pathlib import Path
import json
from main.functions.runHealth import runHealth

import argparse


from main.functions.dynamicAnalysis.dynamic_analysis import DynamicAnalysis
from main.functions.analysis import Analysis, Identifier,FingerprintingMethods
from main.functions.staticAnalysis.static_analysis import StaticAnalysis

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path of datadir directory")
args = parser.parse_args()

def GenerateLogger(filename : Path) -> logging.Logger:
    logger = logging.getLogger('analysis')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - (%(filename)s:%(lineno)d) - %(levelname)s\n%(message)s")
    

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = logging.FileHandler(filename, 'w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def by_visit_id_only(results :Dict[str, Set[Identifier] ]) -> Dict[str, Set[str]]:
    toReturn : Dict[str, Set[str]] = {}
    for k, v in results.items():
        toReturn[k] = set( map(lambda id : id[0], v) )
    return toReturn

def toJSON_serializable(results :Dict[str, Set[Identifier] ]) -> Dict[str, List[Identifier]]:
    return {k : list(v) for k, v in results.items()}

path : Path = Path(args.path)

logger = GenerateLogger(path.joinpath("analysis.log") )

con : sqlite3.Connection = sqlite3.connect( str(path.joinpath("crawl-data.sqlite")) )
db : Any = plyvel.DB( str(path.joinpath("leveldb")) ) # type: ignore

n, f = runHealth(con)
logger.info(f"total visits: {n}, failed/incomplete visits: {f}. Success percentage: {round(100* (1 - f/n)) }%")


SA : Analysis = StaticAnalysis(con, db, logger)
DA : Analysis = DynamicAnalysis(con, db, logger)

DynamicResults = DA.run()
StaticResults = SA.run()

StaticResults_by_visit_id = by_visit_id_only(StaticResults)
DynamicResults_by_visit_id = by_visit_id_only(DynamicResults)

for method in FingerprintingMethods:
    join : Set[Identifier] = DynamicResults[method].intersection(StaticResults[method]) #type: ignore
    logger.info(f"""Fingerprinting method: {method}, 
    in terms of pairs of (visit_id,script_url), 
    dynamically classified: {len(DynamicResults[method])}
    statically classified: {len(StaticResults[method])}
    intersection: {len(join)}
    total dynamically analyzed: {DA.total_identifiers()} 
    total statically analyzed: {SA.total_identifiers()} 
     """)
    join : Set[str] = DynamicResults_by_visit_id[method].intersection( StaticResults_by_visit_id[method])
    logger.info(f"""Fingerprinting method: {method}, 
    in terms of visit_id only, 
    dynamically classified: {len(DynamicResults_by_visit_id[method])}
    statically classified: {len(StaticResults_by_visit_id[method])}
    intersection: {len(join)}
    total visits: {n}
    """)

with open(path.joinpath("dynamic_results.json"),"w") as fileObj:
    fileObj.write( json.dumps( toJSON_serializable(DynamicResults), indent= 4 )  )
with open(path.joinpath("static_results.json"),"w") as fileObj:
    fileObj.write( json.dumps( toJSON_serializable(StaticResults), indent= 4 )  )











