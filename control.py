# control code
import sqlite3
import plyvel
from pathlib import Path
import re
import json
from main.functions.runHealth import runHealth
from main.functions.dynamic_analysis import Dynamic

path : Path = Path('/home/ndanner_plp/OpenWPM/crawl-data/datadir2000')
con : sqlite3.Connection = sqlite3.connect( str(path.joinpath("crawl-data.sqlite")) )
db = plyvel.DB( str(path.joinpath("leveldb")) )

n, f = runHealth(con)
print(f"total visits: {n}, failed/incomplete visits: {f}. Success percentage: {round(100* (1 - f/n)) }%")

results = Dynamic(con)
print( json.dumps( results, indent= 4 ) )

file1 = open("MyFile1.txt","a")
with open(path.joinpath("results.json"),"a") as fileObj:
    fileObj.write( json.dumps( results, indent= 4 )  )
