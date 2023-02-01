from abc import ABC, abstractmethod
import logging

class DynamicAnalysisABC(ABC):
    """
    Base abstract class for an dynamic analysis
    """

    @abstractmethod
    def __init__(self, logger : logging.Logger) -> None:
        """
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        returns fingerprinting method
        """
        pass

    @abstractmethod
    def read_row(self, row : any) -> None:
        """read a single row from """
        pass
    
    @abstractmethod
    def classify(self) -> bool:
        """classify based on rows read"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """reset to the starting state to begin classifying another script """
        pass
