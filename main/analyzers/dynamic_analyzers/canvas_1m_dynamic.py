from typing import Any, List, Set
from analyzers.dynamic_analyzer import Dynamic_Analyzer, parseArguments


class Canvas_1M_Dynamic(Dynamic_Analyzer):
    
    def fingerprinting_type(self) -> str:
        return "Canvas"
    
    def _classify(self) -> bool:
        return (not self._heightORwidthTooSmall) and ( len(self._colors) > 2 or len(self._characters) > 10) and (not self._ProductiveCalls) and self._Extraction

    def _reset(self) -> None :
        # condition 1:
        self._heightORwidthTooSmall : bool = False
        # condition 2:
        self._colors : Set[str] = set()
        self._characters : Set[str] = set()
        # condition 3:
        self._ProductiveCalls : bool = False
        #Condition 4:
        self._Extraction : bool = False

    def _read_row(self, row : Any) -> None:
        parsedArguments: List[Any] = parseArguments(row["arguments"])
        try:
            match row["symbol"]:
                case 'HTMLCanvasElement.height':
                    if row["operation"] == 'set' and row["value"] and float(row["value"]) < 16:
                        self._heightORwidthTooSmall = True
                case 'HTMLCanvasElement.width':
                    if row["operation"] == 'set' and row["value"] and float(row["value"]) < 16:
                        self._heightORwidthTooSmall = True
                case 'CanvasRenderingContext2D.fillText':
                    if len(parsedArguments) > 0:
                        for char in parsedArguments[0]:
                            self._characters.add(char)
                case 'CanvasRenderingContext2D.fillStyle':
                    if row["operation"] == 'set' and row["value"]:
                        self._colors.add(row["value"])
                case 'HTMLCanvasElement.toDataURL':
                    self._Extraction = True
                case 'CanvasRenderingContext2D.getImageData':
                    if len(parsedArguments) > 3:
                        if abs( parsedArguments[2] ) >= 16 and abs( parsedArguments[3] ) >= 16:
                            self._Extraction = True
                case 'HTMLCanvasElement.addEventListener':
                    self._ProductiveCalls = True
                case 'CanvasRenderingContext2D.save':
                    self._ProductiveCalls = True
                case 'CanvasRenderingContext2D.restore':
                    self._ProductiveCalls = True
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")