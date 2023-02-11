from abc import ABC, abstractmethod
import logging
import sqlite3
from typing import Any, List, Tuple

"""
Abstract Base Class for an Analyzer
"""
class Analyzer(ABC):

    def __init__(self, con : sqlite3.Connection, db : Any, logger : logging.Logger) -> None:
        """
        Initialize the analyzer
        """
        self.con: sqlite3.Connection = con
        self.db: Any = db
        self.logger: logging.Logger = logger
    
    def analysis_name(self) -> str:
        """
        returns a unique name among all analyzers representing what analysis is being done
        """
        return self.__class__.__name__
    
    @abstractmethod
    def fingerprinting_type(self) -> str:
        """
        returns name of the fingerprinting method this this analyzer is looking for
        """
        pass
    
    @abstractmethod
    def analysis_domain_size(self) -> int:
        """
        return total number of identifiers (visit_id,script_url) the analysis is being run over
        """
        pass
        
    @abstractmethod
    def analyze(self) -> List[ Tuple[str,str] ]:
        """
        run this analysis, returning a list of (visit_id,script_url) pairs which were classified
        to be doing the fingerprinting method being analyzed
        """
        pass