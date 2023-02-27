import logging
import sqlite3
from typing import Any, List, Set
from analyzers.dynamic_analyzer import Dynamic_Analyzer, parseArguments
from utils.grep_utils import grepForKeywords


class Media_Queries_Dynamic(Dynamic_Analyzer):
    
    def __init__(self, con : sqlite3.Connection, db : Any, logger : logging.Logger) -> None:
        self.__keywords : List[str] = ["dynamic-range", "video-dynamic-range","prefers-color-scheme","prefers-reduced-motion","any-hover",
                                       "color-gamut","forced-colors","inverted-colors", "prefers-contrast"]
        super().__init__(con,db,logger)

    def fingerprinting_type(self) -> str:
        return "Media Queries"
    
    def _classify(self) -> bool:
        # self.logger.info(f"{len(self.__found_keywords)} / {len(self.__keywords)} Media Queries")
        return len(self.__found_keywords) >= len(self.__keywords) - 2 

    def _reset(self) -> None :
        self.__found_keywords : Set[str] = set()

    def _read_row(self, row : Any) -> None:
        parsedArguments: List[Any] = parseArguments(row["arguments"])
        try:
            match row["symbol"]:
                case 'window.matchMedia':
                    if len(parsedArguments) == 1 and type(parsedArguments[0]) == str:
                        self.__found_keywords.update( grepForKeywords(self.__keywords, parsedArguments[0]) )
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}") 
