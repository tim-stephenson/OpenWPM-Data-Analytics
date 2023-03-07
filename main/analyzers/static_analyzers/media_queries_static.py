from typing import List, Any, Set
from sqlalchemy.engine import Engine
import logging
from analyzers.static_analyzer import Static_Analyzer
from utils.grep_utils import grepForKeywords


class Media_Queries_Static(Static_Analyzer):


    def __init__(self, engine : Engine, db : Any, logger : logging.Logger) -> None:
        self.__keywords : List[str] = [".matchMedia", "matchMedia",
                                        "dynamic-range", "video-dynamic-range","prefers-color-scheme","prefers-reduced-motion","any-hover",
                                       "color-gamut","forced-colors","inverted-colors", "prefers-contrast"]
        super().__init__(engine,db,logger)

    def fingerprinting_type(self) -> str:
        return "Media Queries"
    
    def _analyze_one(self,source_code : str) -> bool:
        results: Set[str] = grepForKeywords(self.__keywords, source_code) 

        function_call : bool = results.__contains__(".matchMedia") or results.__contains__("matchMedia")
        results.discard(".matchMedia")
        results.discard("matchMedia")
        media_keywords : int = len(results)
        # self.logger.info(f"matchMedia: {function_call}\n{media_keywords} / {len(self.__keywords)-2} Media Queries")
        return function_call and media_keywords >= len(self.__keywords) - 4