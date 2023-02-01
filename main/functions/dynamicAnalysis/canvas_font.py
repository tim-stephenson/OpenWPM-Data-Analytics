import ast
from typing import Any, Dict, Set
import logging

from functions.dynamicAnalysis.dynamic_analysis_ABC import DynamicAnalysisABC     


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

    def read_row(self, row : Any) -> None:
        """read a single row from """
        args = None
        try:
            if row["arguments"] is not None:
                args = ast.literal_eval(row["arguments"])
        except ValueError:
            self.logger.info(f"""Was unable to parse function arguments, row.arguments : {row["arguments"]}""")
        try:
            match row["symbol"]:
                case 'CanvasRenderingContext2D.font':
                    if row["operation"] == 'set' and row["value"]:
                        self.fonts.add(row["value"])
                case 'CanvasRenderingContext2D.measureText':
                    if row["operation"] == 'call' and args and len(args)==1:
                        self.textMeasured[args[0]] = 1 + (self.textMeasured[args[0]] if args[0] in self.textMeasured else 0)
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")


    def classify(self) -> bool:
        """classify based on rows read"""
        self.logger.info(f"fonts: {len( self.fonts)}   measureText calls : { max(self.textMeasured.values()) if len( self.textMeasured) > 0 else 0 } ")
        return len( self.fonts) >= 50 and (  ( max( self.textMeasured.values()) if len( self.textMeasured) > 0 else 0 ) >= 50 )

    def reset(self) -> None:
        """reset to the starting state to begin classifying another script """
        self.fonts : Set[str] = set()
        self.textMeasured : Dict[str, int] = dict()
        