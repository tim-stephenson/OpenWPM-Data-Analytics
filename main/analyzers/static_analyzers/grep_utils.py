
import re
from typing import Dict, List


def grepForKeywords(keywords : List[str],  s : str) -> Dict[str, bool]:
    results : Dict[str, bool] = { keyword : False for keyword in keywords}
    for keyword in keywords:
        if re.search(re.escape(keyword),s) is not None:
            results[keyword] = True
    return results

# def compile_regex_from_keywords(keywords : List[str]) -> re.Pattern[str]:
#     pattern: str = "|".join(map(lambda keyword : "(" + re.escape(keyword) + ")", keywords))
#     return re.compile(pattern)