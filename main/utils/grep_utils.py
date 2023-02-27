
import re
from typing import Set, List


def grepForKeywords(keywords : List[str],  s : str) -> Set[str]:
    results : Set[str] = set()
    for keyword in keywords:
        if re.search(re.escape(keyword),s) is not None:
            results.add(keyword)
    return results

# def compile_regex_from_keywords(keywords : List[str]) -> re.Pattern[str]:
#     pattern: str = "|".join(map(lambda keyword : "(" + re.escape(keyword) + ")", keywords))
#     return re.compile(pattern)