import logging
import re


def Canvas(code : str, logger : logging.Logger):
    keywords = ["\\.toDataURL", "\\.getImageData", "\\.addEventListener",
    "\\.save", "\\.restore", "\\.fillStyle", "\\.fillText", 
    "\\.width", "\\.height" ]
    pattern = "|".join(map(lambda s : "(" + s + ")", keywords))
    # condition 1 (not trivial implementation):

    # condition 2 (trivially assume they use enough characters/
    # colors for the script to be counted):
    colors : bool = False
    characters : bool = False

    # condition 3 (for not not using it, is seems to classy 
    # almost every actually fingerprinting script as productive ):
    # ProductiveCalls : bool = False

    #Condition 4:
    Extraction : bool = False
    for m in re.finditer(pattern,code):
        match m[0]:
            case ".height":
                pass
            case ".width":
                pass
            case ".fillText":
                characters = True
            case ".fillStyle":
                colors = True
            case ".toDataURL":
                Extraction = True
            case ".getImageData":
                Extraction = True
            case ".addEventListener":
                # ProductiveCalls = True
                pass
            case ".save":
                # ProductiveCalls = True
                pass
            case ".restore":
                # ProductiveCalls = True
                pass
            case _:
                pass

    #    condition 2                  condition 4
    return  ( colors and characters)  and Extraction