from typing import Any, Dict, List, Set
from analyzers.dynamic_analyzer import Dynamic_Analyzer, parseArguments


class Canvas_Font_1M_Dynamic(Dynamic_Analyzer):
    
    @staticmethod
    def fingerprinting_type() -> str:
        return "Canvas Font"
    
    def _classify(self) -> bool:
        return len( self.__fonts) >= 50 and ( max(self.__textMeasured.values(), default=0) >= 50 )

    def _reset(self) -> None :
        self.__fonts : Set[str] = set()
        self.__textMeasured : Dict[str, int] = dict()

    def _read_row(self, row : Any) -> None:
        parsedArguments: List[Any] = parseArguments(row["arguments"])
        try:
            match row["symbol"]:
                case 'CanvasRenderingContext2D.font':
                    if row["operation"] == 'set' and row["value"]:
                        self.__fonts.add(row["value"])
                case 'CanvasRenderingContext2D.measureText':
                    if row["operation"] == 'call' and len(parsedArguments) > 0:
                        if parsedArguments[0] in self.__textMeasured:
                            self.__textMeasured[parsedArguments[0]] += 1
                        else:
                            self.__textMeasured[parsedArguments[0]] = 1
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}") 