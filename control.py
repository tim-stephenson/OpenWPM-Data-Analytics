# control code
import logging
import sqlite3
import plyvel
from pathlib import Path
import json
from main.functions.runHealth import runHealth

import argparse

from main.functions.dynamic_analysis import DynamicAnalysis
from main.functions.static_analysis import StaticAnalysis

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path of datadir directory")
args = parser.parse_args()

def GenerateLogger(filename : Path) -> logging.Logger:
    logger = logging.getLogger('analysis')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)")
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s:\n%(message)s')
    

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = logging.FileHandler(filename, 'w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


path : Path = Path(args.path)

logger = GenerateLogger(path.joinpath("analysis.log") )

con : sqlite3.Connection = sqlite3.connect( str(path.joinpath("crawl-data.sqlite")) )
db = plyvel.DB( str(path.joinpath("leveldb")) )

n, f = runHealth(con)
logger.info(f"total visits: {n}, failed/incomplete visits: {f}. Success percentage: {round(100* (1 - f/n)) }%")


SA = StaticAnalysis(con, db, logger)
DA = DynamicAnalysis(con, db, logger)

StaticResults = SA.run()
DynamicResults = DA.run()




with open(path.joinpath("dynamic_results.json"),"w") as fileObj:
    fileObj.write( json.dumps( DynamicResults, indent= 4 )  )
with open(path.joinpath("static_results.json"),"w") as fileObj:
    fileObj.write( json.dumps( StaticResults, indent= 4 )  )




