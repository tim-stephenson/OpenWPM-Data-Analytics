
import logging
import re


def WebGL(code : str, logger : logging.Logger) -> bool:
    keywords = ["\\.getParameter"]
    pattern = "|".join(map(lambda s : "(" + s + ")", keywords))


    con1 : bool = False
    for m in re.finditer(pattern,code):
        match m[0]:
            case ".getParameter":
                con1 = True
            case _:
                pass
    return con1
