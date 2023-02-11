from typing import Any, List, Set
from analyzers.dynamic_analyzer import Dynamic_Analyzer, parseArguments


class Canvas_1M_Dynamic(Dynamic_Analyzer):
    
    def fingerprinting_type(self) -> str:
        return "Canvas"
    
    def _classify(self) -> bool:
        return (not self.heightORwidthTooSmall) and ( len(self.colors) > 2 or len(self.characters) > 10) and (not self.ProductiveCalls) and self.Extraction

    def _reset(self) -> None :
        # condition 1:
        self.heightORwidthTooSmall : bool = False
        # condition 2:
        self.colors : Set[str] = set()
        self.characters : Set[str] = set()
        # condition 3:
        self.ProductiveCalls : bool = False
        #Condition 4:
        self.Extraction : bool = False

    def _read_row(self, row : Any) -> None:
        parsedArguments: List[Any] = parseArguments(row["arguments"])
        try:
            match row["symbol"]:
                case 'HTMLCanvasElement.height':
                    if row["operation"] == 'set' and row["value"] and float(row["value"]) < 16:
                        self.heightORwidthTooSmall = True
                case 'HTMLCanvasElement.width':
                    if row["operation"] == 'set' and row["value"] and float(row["value"]) < 16:
                        self.heightORwidthTooSmall = True
                case 'CanvasRenderingContext2D.fillText':
                    if len(parsedArguments) > 0:
                        for char in parsedArguments[0]:
                            self.characters.add(char)
                case 'CanvasRenderingContext2D.fillStyle':
                    if row["operation"] == 'set' and row["value"]:
                        self.colors.add(row["value"])
                case 'HTMLCanvasElement.toDataURL':
                    self.Extraction = True
                case 'CanvasRenderingContext2D.getImageData':
                    if len(parsedArguments) > 3:
                        if abs( parsedArguments[2] ) >= 16 and abs( parsedArguments[3] ) >= 16:
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