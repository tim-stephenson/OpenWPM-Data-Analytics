from abc import ABC, abstractmethod
import sqlite3
import logging
from typing import Dict, Set, Tuple, Any

# (visit_id, script_url)
Identifier = Tuple[str,str]


FingerprintingMethods: list[str] = ["Canvas", "WebRTC", "CanvasFont","WebGL"]
# FingerprintingMethods2: list[str] = ["Canvas_1M_Dynamic", "WebRTC_1M_Dynamic", "CanvasFont_1M_Dynamic", "WebGL_Dynamic" ]

class Analysis(ABC):
    """
    Base abstract class for an analysis
    """

    @abstractmethod
    def __init__(self, con : sqlite3.Connection, db : Any, logger : logging.Logger) -> None:
        """"""
        pass

    @abstractmethod
    def total_identifiers(self) -> int:
        """return total number of identifiers (visit_id,script_url) the analysis is being run over"""
        pass

    @abstractmethod
    def run(self) -> Dict[str, Set[Identifier] ]:
        """run analysis"""
        pass





