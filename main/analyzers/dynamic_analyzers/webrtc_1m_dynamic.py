from typing import Any
from analyzers.dynamic_analyzer import Dynamic_Analyzer


class WebRTC_1M_Dynamic(Dynamic_Analyzer):
    
    def fingerprinting_type(self) -> str:
        return "WebRTC"
    
    def _classify(self) -> bool:
        return self._con1 and self._con2 and self._con3

    def _reset(self) -> None :
        self._con1 : bool = False
        self._con2 : bool = False
        self._con3 : bool = False

    def _read_row(self, row : Any) -> None:
        try:
            match row["symbol"]:
                case 'RTCPeerConnection.createDataChannel':
                    self._con1 = True
                case 'RTCPeerConnection.createOffer':
                    self._con2 = True
                case 'RTCPeerConnection.onicecandidate':
                    self._con3 = True
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")