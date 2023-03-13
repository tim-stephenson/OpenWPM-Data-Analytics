from abc import ABC, abstractmethod
import logging
from sqlalchemy.engine import Engine
from typing import Any, List, Tuple

"""
Abstract Base Class for an Analyzer
"""
class Analyzer(ABC):

    def __init__(self, engine : Engine, db : Any, logger : logging.Logger) -> None:
        """
        Initialize the analyzer
        """
        self.engine: Engine = engine
        self.db: Any = db
        self.logger: logging.Logger = logger
        self.results : None | List[ Tuple[str,str] ] = None
    
    @classmethod
    def analysis_name(cls) -> str:
        """
        returns a unique name among all analyzers representing what analysis is being done
        """
        return cls.__name__
    
    @staticmethod
    @abstractmethod
    def fingerprinting_type() -> str:
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
    def analysis_domain(self) ->  List[ Tuple[str,str] ]:
        """
        return all identifiers (visit_id,script_url) the analysis is being run over
        """
        pass
        
    
    def run_analysis(self) -> None:
        """
        manually trigger a run of the analysis.
        results are accessible via 'get_analysis_results'
        """
        self.results = self._analyze()

    @abstractmethod
    def _analyze(self) -> List[ Tuple[str,str] ]:
        """
        run this analysis, returning a list of (visit_id,script_url) pairs which were classified
        to be doing the fingerprinting method being analyzed
        """
        pass
    
    def get_analysis_results(self) -> List[ Tuple[str,str] ]:
        """
        get the analysis results.
        runs the run_analysis method if no results are currently available
        """
        if self.results is None:
            self.results = self._analyze()
        return self.results
    
    def set_analysis_results(self, results: List[ Tuple[str,str] ]) -> None:
        """
        manually set the analysis results.
        typically used to restore the cache from a previous analysis
        """
        self.results = results