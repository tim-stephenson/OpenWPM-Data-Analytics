from typing import Any
from analyzers.dynamic_analyzer import Dynamic_Analyzer


class WebRTC_1M_Dynamic(Dynamic_Analyzer):
    
    def fingerprinting_type(self) -> str:
        return "WebRTC"
    
    def _classify(self) -> bool:
        return self.con1 and self.con2 and self.con3

    def _reset(self) -> None :
        self.con1 : bool = False
        self.con2 : bool = False
        self.con3 : bool = False

    def _read_row(self, row : Any) -> None:
        try:
            match row["symbol"]:
                case 'RTCPeerConnection.createDataChannel':
                    self.con1 = True
                case 'RTCPeerConnection.createOffer':
                    self.con2 = True
                case 'RTCPeerConnection.onicecandidate':
                    self.con3 = True
                case _:
                    pass
        except Exception as e:
            self.logger.exception(f"Found Exception {e}, row: {row}")