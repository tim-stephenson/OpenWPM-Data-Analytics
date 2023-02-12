from typing import Any
from analyzers.dynamic_analyzer import Dynamic_Analyzer


class WebRTC_1M_Dynamic(Dynamic_Analyzer):
    
    def fingerprinting_type(self) -> str:
        return "WebRTC"
    
    def _classify(self) -> bool:
        return self.__con1 and self.__con2 and self.__con3

    def _reset(self) -> None :
        self.__con1 : bool = False
        self.__con2 : bool = False
        self.__con3 : bool = False

    def _read_row(self, row : Any) -> None:
        try:
            match row["symbol"]:
                case 'RTCPeerConnection.createDataChannel':
                    self.__con1 = True
                case 'RTCPeerConnection.createOffer':
                    self.__con2 = True
                case 'RTCPeerConnection.onicecandidate':
                    self.__con3 = True
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")