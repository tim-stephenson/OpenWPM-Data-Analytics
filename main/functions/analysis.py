from abc import ABC, abstractmethod
import sqlite3
import logging
from typing import Dict, List, Tuple

# (visit_id, script_url)
Identifier = Tuple[str,str]

class Analysis(ABC):
    """
    Base abstract class for an analysis
    """

    @abstractmethod
    def __init__(self, con : sqlite3.Connection, db : any, logger : logging.Logger) -> None:
        """"""
        pass

    @abstractmethod
    def run(self) -> Dict[str, List[Identifier] ]:
        """run analysis"""
        pass


