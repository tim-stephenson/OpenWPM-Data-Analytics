from typing import Any, Dict, List, Set
from analyzers.dynamic_analyzer import Dynamic_Analyzer, parseArguments


class Canvas_Font_1M_Dynamic(Dynamic_Analyzer):
    
    def fingerprinting_type(self) -> str:
        return "Canvas Font"
    
    def _classify(self) -> bool:
        return len( self.fonts) >= 50 and ( max(self.textMeasured.values(), default=0) >= 50 )

    def _reset(self) -> None :
        self.fonts : Set[str] = set()
        self.textMeasured : Dict[str, int] = dict()

    def _read_row(self, row : Any) -> None:
        parsedArguments: List[Any] = parseArguments(row["arguments"])
        try:
            match row["symbol"]:
                case 'CanvasRenderingContext2D.font':
                    if row["operation"] == 'set' and row["value"]:
                        self.fonts.add(row["value"])
                case 'CanvasRenderingContext2D.measureText':
                    if row["operation"] == 'call' and len(parsedArguments) > 0:
                        if parsedArguments[0] in self.textMeasured:
                            self.textMeasured[parsedArguments[0]] += 1
                        else:
                            self.textMeasured[parsedArguments[0]] = 1
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}") 