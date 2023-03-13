from typing import Any, List
from analyzers.dynamic_analyzer import Dynamic_Analyzer, parseArguments


class Canvas_Basic_Dynamic(Dynamic_Analyzer):
    
    @staticmethod
    def fingerprinting_type() -> str:
        return "Canvas"
    
    def _classify(self) -> bool:
        return ( max(self.__heights,default=150) >= 16 and max(self.__widths,default=300) >= 16 ) and \
        max( map(lambda s : len(set(s)), self.__characters),default=0) >= 10 and \
         self.__Extraction

    def _reset(self) -> None :
        self.__heights : List[float] = []
        self.__widths : List[float] = []

        self.__characters : List[str] = []

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
                    if len(parsedArguments) >= 1 and type(parsedArguments[0])==str:
                        self.__characters.append(parsedArguments[0])
                case 'HTMLCanvasElement.toDataURL':
                    self.__Extraction = True
                case 'CanvasRenderingContext2D.getImageData':
                    if len(parsedArguments) >= 4:
                        if abs( float(parsedArguments[2]) ) >= 16 and abs( float(parsedArguments[3]) ) >= 16:
                            self.__Extraction = True
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")