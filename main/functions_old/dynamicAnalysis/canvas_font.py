from typing import Any, Dict, Set
import logging

from functions_old.dynamicAnalysis.dynamic_analysis_ABC import DynamicAnalysisABC     


class CanvasFont(DynamicAnalysisABC):
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
        return "CanvasFont"

    def read_row(self, row : Any, parsedArguments : Any | None) -> None:
        """read a single row from """
        try:
            match row["symbol"]:
                case 'CanvasRenderingContext2D.font':
                    if row["operation"] == 'set' and row["value"]:
                        self.fonts.add(row["value"])
                case 'CanvasRenderingContext2D.measureText':
                    if row["operation"] == 'call' and parsedArguments and len(parsedArguments)==1:
                        self.textMeasured[parsedArguments[0]] = 1 + (self.textMeasured[parsedArguments[0]] if parsedArguments[0] in self.textMeasured else 0)
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")


    def classify(self) -> bool:
        """classify based on rows read"""
        if len( self.fonts) > 0 or max(self.textMeasured.values(), default=0) > 0:
            self.logger.info(f"fonts: {len( self.fonts)}   measureText calls : { max(self.textMeasured.values(), default=0) } ")
        return len( self.fonts) >= 50 and ( max(self.textMeasured.values(), default=0) >= 50 )

    def reset(self) -> None:
        """reset to the starting state to begin classifying another script """
        self.fonts : Set[str] = set()
        self.textMeasured : Dict[str, int] = dict()
        