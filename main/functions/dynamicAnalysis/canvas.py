from typing import Any, Set
from functions.dynamicAnalysis.dynamic_analysis_ABC import DynamicAnalysisABC
import ast
import logging      


class Canvas(DynamicAnalysisABC):
    """
    """

    def __init__(self, logger : logging.Logger) -> None:
        """
        """
        self.logger : logging.Logger  = logger
        self.reset()

    def __str__(self) -> str:
        """
        returns fingerprinting method
        """
        return "Canvas"

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
                case 'HTMLCanvasElement.height':
                    if row["operation"] == 'set' and row["value"] and float(row["value"]) < 16:
                        self.heightORwidthTooSmall = True
                case 'HTMLCanvasElement.width':
                    if row["operation"] == 'set' and row["value"] and float(row["value"]) < 16:
                        self.heightORwidthTooSmall = True
                case 'CanvasRenderingContext2D.fillText':
                    if args is not None:
                        for char in args[0]:
                            self.characters.add(char)
                case 'CanvasRenderingContext2D.fillStyle':
                    if row["operation"] == 'set' and row["value"]:
                        self.colors.add(row["value"])
                case 'HTMLCanvasElement.toDataURL':
                    self.Extraction = True
                case 'CanvasRenderingContext2D.getImageData':
                    if args is not None:
                        if abs( args[2] ) >= 16 and abs( args[3] ) >= 16:
                            self.Extraction = True
                case 'HTMLCanvasElement.addEventListener':
                    self.ProductiveCalls = True
                case 'CanvasRenderingContext2D.save':
                    self.ProductiveCalls = True
                case 'CanvasRenderingContext2D.restore':
                    self.ProductiveCalls = True
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")

    def classify(self) -> bool:
        """classify based on rows read"""
        return (not self.heightORwidthTooSmall) and ( len(self.colors) > 2 or len(self.characters) > 10) and (not self.ProductiveCalls) and self.Extraction
    
    def reset(self) -> None:
        """reset to the starting state to begin classifying another script """
        # condition 1:
        self.heightORwidthTooSmall : bool = False
        # condition 2:
        self.colors : Set[str] = set()
        self.characters : Set[str] = set()
        # condition 3:
        self.ProductiveCalls : bool = False
        #Condition 4:
        self.Extraction : bool = False