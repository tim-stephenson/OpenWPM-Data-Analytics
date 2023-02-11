from typing import Any
from functions_old.dynamicAnalysis.dynamic_analysis_ABC import DynamicAnalysisABC   
import logging      

class WebRTC(DynamicAnalysisABC):
    """
    """

    def __init__(self, logger : logging.Logger) -> None:
        """
        """
        self.logger = logger
        self.reset()


    def __str__(self) -> str:
        """
        returns fingerprinting method
        """
        return "WebRTC"

    def read_row(self, row : Any, parsedArguments : Any | None) -> None:
        """read a single row from """
        try:
            match row["symbol"]:
                case 'RTCPeerConnection.createDataChannel':
                    self.con1 = True
                case 'RTCPeerConnection.createOffer':
                    self.con2 = True
                case 'RTCPeerConnection.onicecandidate':
                    self.con3 = True
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")


    def classify(self) -> bool:
        """classify based on rows read"""
        return self.con1 and self.con2 and self.con3
    
    def reset(self) -> None:
        """reset to the starting state to begin classifying another script """
        self.con1 : bool = False
        self.con2 : bool = False
        self.con3 : bool = False
