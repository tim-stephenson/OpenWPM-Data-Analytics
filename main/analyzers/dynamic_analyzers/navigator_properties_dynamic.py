import collections
import logging
import sqlite3
from typing import Any, Set
from analyzers.dynamic_analyzer import Dynamic_Analyzer



class Navigator_Properties_Dynamic(Dynamic_Analyzer):
    
    def __init__(self, con : sqlite3.Connection, db : Any, logger : logging.Logger) -> None:
        self.__properties : Set[str] = set(["window.navigator.storage.estimate","window.navigator.mediaDevices.enumerateDevices", 
                                         "window.navigator.hardwareConcurrency","window.navigator.language","window.navigator.maxTouchPoints"])
        super().__init__(con,db,logger)

    def fingerprinting_type(self) -> str:
        return "Navigator Properties"
    
    def _classify(self) -> bool:
        self.logger.info(f"Navigator Properties Counts:\n{self.__found_properties_counts}")
        return len(self.__found_properties_counts) >= len(self.__properties) - 2 

    def _reset(self) -> None :
        self.__found_properties_counts : collections.Counter[str] = collections.Counter()

    def _read_row(self, row : Any) -> None:
        try:
            if self.__properties.__contains__(row["symbol"]):
                self.__found_properties_counts[row["symbol"]] += 1
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}") 