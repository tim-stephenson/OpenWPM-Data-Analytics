# control code
import sqlite3
import plyvel
from pathlib import Path
import re
import json
from main.functions.runHealth import runHealth
from main.functions.dynamic_analysis import Dynamic
import argparse

from main.functions.static_analysis import Static
parser = argparse.ArgumentParser()
parser.add_argument("path", help="path of datadir directory")
args = parser.parse_args()


path : Path = Path(args.path)

con : sqlite3.Connection = sqlite3.connect( str(path.joinpath("crawl-data.sqlite")) )
db = plyvel.DB( str(path.joinpath("leveldb")) )

n, f = runHealth(con)
print(f"total visits: {n}, failed/incomplete visits: {f}. Success percentage: {round(100* (1 - f/n)) }%")

DynamicResults = Dynamic(con)
StaticResults = Static(con, db)




with open(path.joinpath("dynamic_results.json"),"w") as fileObj:
    fileObj.write( json.dumps( DynamicResults, indent= 4 )  )
with open(path.joinpath("static_results.json"),"w") as fileObj:
    fileObj.write( json.dumps( StaticResults, indent= 4 )  )
