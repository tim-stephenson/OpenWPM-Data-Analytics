from typing import Any
from functions_old.dynamicAnalysis.dynamic_analysis_ABC import DynamicAnalysisABC   
import logging      

class WebGL(DynamicAnalysisABC):
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
        return "WebGL"

    def read_row(self, row : Any, parsedArguments : Any | None) -> None:
        """read a single row from """
        try:
            match row["symbol"]:
                case 'WebGLRenderingContext.getParameter':
                    if parsedArguments is not None and len(parsedArguments) >= 1 and ( parsedArguments[0] == 37445 or parsedArguments[0] == 37446):
                        self.con1 = True
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")


    def classify(self) -> bool:
        """classify based on rows read"""
        return self.con1
    
    def reset(self) -> None:
        """reset to the starting state to begin classifying another script """
        self.con1 : bool = False