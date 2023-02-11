import logging
import re


def WebRTC(code : str, logger : logging.Logger):
    keywords = ["\\.createDataChannel", "\\.createOffer", "\\.onicecandidate"]
    pattern = "|".join(map(lambda s : "(" + s + ")", keywords))


    con1 : bool = False
    con2 : bool = False
    con3 : bool = False
    for m in re.finditer(pattern,code):
        match m[0]:
            case ".createDataChannel":
                con1 = True
            case ".createOffer":
                con2 = True
            case ".onicecandidate":
                con3 = True
            case _:
                pass
    return con1 and con2 and con3
