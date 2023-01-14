import pandas as pd
import logging      


def WebRTC(df :  pd.DataFrame, logger : logging.Logger) -> bool:

    con1 : bool = False
    con2 : bool = False
    con3 : bool = False
    for row in df.itertuples():
        try:
            match row.symbol:
                case 'RTCPeerConnection.createDataChannel':
                    con1 = True
                case 'RTCPeerConnection.createOffer':
                    con2 = True
                case 'RTCPeerConnection.onicecandidate':
                    con3 = True
        except Exception as e:
            logger.exception(f"Found Exception {e}, row: {row}")
    return con1 and con2 and con3