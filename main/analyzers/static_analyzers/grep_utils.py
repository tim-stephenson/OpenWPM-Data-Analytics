
import re
from typing import Dict, List


def grepForKeywords(keywords : List[str], s : str) -> Dict[str, bool]:
    pattern: str = "|".join(map(lambda keyword : "(" + re.escape(keyword) + ")", keywords))
    results : Dict[str, bool] = { keyword : False for keyword in keywords}

    for m in re.finditer(pattern,s):
        results[m[0]] = True

    return results