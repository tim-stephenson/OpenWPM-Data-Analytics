
import re
from typing import Set, List, Match


def grepForKeywords(keywords : List[str],  s : str) -> Set[str]:
    results : Set[str] = set()
    for keyword in keywords:
        if re.search(re.escape(keyword),s) is not None:
            results.add(keyword)
    return results

# def compile_regex_from_keywords(keywords : List[str]) -> re.Pattern[str]:
#     pattern: str = "|".join(map(lambda keyword : "(" + re.escape(keyword) + ")", keywords))
#     return re.compile(pattern)


# un-escape characters escaped via any of the three methods:
# \xXX                                                       i.e.    \x4E = N          \x21 = !
# \uXXXX                                                     i.e.    \u265A = ♚        \u269B = ⚛
# \u{X} \u{XX} \u{XXX} \u{XXXX} \u{XXXXXX} \u{XXXXXX}        i.e.    \u{1F603} = 😃     \u{20457}= 𠑗 
# 
# source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String#escape_sequences
def unescapeString(s : str) -> str:
    pattern : str = r"\\x[a-fA-F0-9]{2}|\\u[a-fA-F0-9]{4}|\\u\{[a-fA-F0-9]{1,6}\}"
    return re.sub(pattern, replacement_function, s)


def replacement_function(m : Match[str] ) -> str:
    s : str = m.string[m.start(0):m.end(0)]
    if s[1] == 'x':
        value = int(s[2:4], 16)
    elif s[2] == '{':
        value = int(s[3:-1], 16)
    else:
        value = int(s[2:6], 16)
    return chr(value)

