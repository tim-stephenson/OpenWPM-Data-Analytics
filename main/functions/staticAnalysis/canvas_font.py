import logging
import re


def CanvasFont(code : str, logger : logging.Logger):
    keywords = ["\\.measureText", "\\.font"]
    pattern = "|".join(map(lambda s : "(" + s + ")", keywords))


    con1 : bool = False
    con2 : bool = False
    for m in re.finditer(pattern,code):
        match m[0]:
            case ".measureText":
                con1 = True
            case ".font":
                con2 = True
    return con1 and con2
