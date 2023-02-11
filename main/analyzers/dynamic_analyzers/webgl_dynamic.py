from typing import Any, List
from analyzers.dynamic_analyzer import Dynamic_Analyzer, parseArguments


class WebGL_Dynamic(Dynamic_Analyzer):
    
    def fingerprinting_type(self) -> str:
        return "WebGL"
    
    def _classify(self) -> bool:
        return self._con1

    def _reset(self) -> None :
        self._con1 : bool = False

    def _read_row(self, row : Any) -> None:
        parsedArguments: List[Any] = parseArguments(row["arguments"])
        try:
            match row["symbol"]:
                case 'WebGLRenderingContext.getParameter':
                    if len(parsedArguments) >= 1 and ( parsedArguments[0] == 37445 or parsedArguments[0] == 37446):
                        self._con1 = True
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")