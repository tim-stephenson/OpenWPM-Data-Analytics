from typing import List, Any, Set
from sqlalchemy.engine import Engine
import logging
from analyzers.static_analyzer import Static_Analyzer
from utils.grep_utils import grepForKeywords, unescapeString

class Canvas_Basic_Static_2(Static_Analyzer):


    def __init__(self, engine : Engine, db : Any, logger : logging.Logger) -> None:
        self.__keywords : List[str] = ["toDataURL", "getImageData", "fillText","strokeText"]
        super().__init__(engine,db,logger)

    @staticmethod
    def fingerprinting_type() -> str:
        return "Canvas"
    
    def _analyze_one(self,source_code : str) -> bool:
        source_code_escaped : str =  unescapeString(source_code)

        results: Set[str] = grepForKeywords(self.__keywords, source_code_escaped) #type: ignore

        characters : bool = results.__contains__("fillText") or results.__contains__("strokeText")
        Extraction : bool = results.__contains__("toDataURL") or results.__contains__("getImageData")
        return characters and Extraction