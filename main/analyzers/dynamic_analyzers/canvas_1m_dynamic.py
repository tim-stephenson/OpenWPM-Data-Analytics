from typing import Any, List, Set
from analyzers.dynamic_analyzer import Dynamic_Analyzer, parseArguments


class Canvas_1M_Dynamic(Dynamic_Analyzer):
    
    @staticmethod
    def fingerprinting_type() -> str:
        return "Canvas"
    
    def _classify(self) -> bool:
        return ( max(self.__heights,default=150) >= 16 and max(self.__widths,default=300) >= 16 ) and \
        ( len(self.__colors) > 2 or len(self.__characters) > 10) and \
        (not self.__ProductiveCalls) and self.__Extraction

    def _reset(self) -> None :
        # condition 1:
        self.__heightORwidthTooSmall : bool = False
        self.__heights : List[float] = []
        self.__widths : List[float] = []
        # condition 2:
        self.__colors : Set[str] = set()
        self.__characters : Set[str] = set()
        # condition 3:
        self.__ProductiveCalls : bool = False
        #Condition 4:
        self.__Extraction : bool = False

    def _read_row(self, row : Any) -> None:
        parsedArguments: List[Any] = parseArguments(row["arguments"])
        try:
            match row["symbol"]:
                case 'HTMLCanvasElement.height':
                    if row["operation"] == 'set' and row["value"]:
                        self.__heights.append(float(row["value"]))
                case 'HTMLCanvasElement.width':
                    if row["operation"] == 'set' and row["value"]:
                        self.__widths.append(float(row["value"]))
                case 'CanvasRenderingContext2D.fillText':
                    if len(parsedArguments) >= 1:
                        for char in parsedArguments[0]:
                            self.__characters.add(char)
                case 'CanvasRenderingContext2D.fillStyle':
                    if row["operation"] == 'set' and row["value"]:
                        self.__colors.add(row["value"])
                case 'HTMLCanvasElement.toDataURL':
                    self.__Extraction = True
                case 'CanvasRenderingContext2D.getImageData':
                    if len(parsedArguments) >= 4:
                        if abs( parsedArguments[2] ) >= 16 and abs( parsedArguments[3] ) >= 16:
                            self.__Extraction = True
                case 'HTMLCanvasElement.addEventListener':
                    self.__ProductiveCalls = True
                case 'CanvasRenderingContext2D.save':
                    self.__ProductiveCalls = True
                case 'CanvasRenderingContext2D.restore':
                    self.__ProductiveCalls = True
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")