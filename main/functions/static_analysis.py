
import functools
import logging
import re
import sqlite3
from typing import Dict, List
import jsbeautifier
from main.functions.analysis import Analysis, Identifier


class StaticAnalysis(Analysis):

    def __init__(self, con : sqlite3.Connection, db : any, logger : logging.Logger) -> None:
        self.con = con
        self.db = db
        self.logger = logger
    
    def run(self) -> Dict[str, List[Identifier] ]:
        self.count_unique = 0
        
        numEntries : sqlite3.Cursor = self.con.cursor().execute(
            """SELECT COUNT(visit_id)
            FROM http_responses 
            WHERE content_hash <> "" """
            )
        n : int = numEntries.fetchone()[0]
        responses : sqlite3.Cursor = self.con.cursor().execute(
            """SELECT id, visit_id, headers, url, content_hash
            FROM http_responses 
            WHERE content_hash <> "" """
            )
        responses.row_factory = sqlite3.Row
        results : Dict[str, List[Identifier] ] = {
            "Canvas" : []
        }
        i : int = 0
        for row in responses:
            if(i % 1000 == 0):
                self.logger.info(f"Done: {i} out of {n}")
            i += 1

            script_analyze_results : List[str] = self._Analyze(bytes( row["content_hash"], encoding="ascii" ))
            id : Identifier = (row["visit_id"], row["url"] )
            for fingerprintingMethod in script_analyze_results:
                self.logger.info(f"found: {id} ")
                results[fingerprintingMethod].append(id)
    
        self.logger.info(f"unique: {self.count_unique}, n : {n}")
        return results

    @functools.cache
    def _Analyze(self,content_hash : bytes) -> List[str]:
        self.count_unique += 1
        try:
            code : str = str( self.db.get(content_hash  ) ,encoding="UTF-8")
        except Exception as e:
            self.logger.exception(f"Found Exception {e}")
            return []
        # code : str = jsbeautifier.beautify(code)
        toReturn : List[str] = []
        if self._Canvas(code):
            toReturn.append("Canvas")
        return toReturn

    def _Canvas(self, code : str):
        keywords = ["\\.toDataURL", "\\.getImageData", "\\.addEventListener",
        "\\.save", "\\.restore", "\\.fillStyle", "\\.fillText", 
        "\\.width", "\\.height" ]
        pattern = "|".join(map(lambda s : "(" + s + ")", keywords))
        # condition 1 (not trivial implementation):

        # condition 2 (trivially assume they use enough characters/
        # colors for the script to be counted):
        colors : bool = False
        characters : bool = False

        # condition 3 (for not not using it, is seems to classy 
        # almost every actually fingerprinting script as productive ):
        # ProductiveCalls : bool = False

        #Condition 4:
        Extraction : bool = False
        try:
            for m in re.finditer(pattern,code):
                match m[0]:
                    case ".height":
                        pass
                    case ".width":
                        pass
                    case ".fillText":
                        characters = True
                    case ".fillStyle":
                        colors = True
                    case ".toDataURL":
                        Extraction = True
                    case ".getImageData":
                        Extraction = True
                    case ".addEventListener":
                        # ProductiveCalls = True
                        pass
                    case ".save":
                        # ProductiveCalls = True
                        pass
                    case ".restore":
                        # ProductiveCalls = True
                        pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}")

        #    condition 2                  condition 4
        return  ( colors and characters)  and Extraction















"""
    # build
    subprocess.run(["sh", "node/run.sh", "npm run build"])
    completedProcess : subprocess.CompletedProcess = subprocess.run(["sh", "node/run.sh", f"npm run execute \"{code}\""])

"""