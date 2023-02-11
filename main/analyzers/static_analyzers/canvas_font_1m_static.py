from typing import Dict
from analyzers.static_analyzer import Static_Analyzer
from analyzers.static_analyzers.grep_utils import grepForKeywords


class Canvas_Font_1M_Static(Static_Analyzer):

    def fingerprinting_type(self) -> str:
        return "Canvas Font"
    
    def _analyze_one(self,source_code : str) -> bool:
        results: Dict[str, bool] = grepForKeywords(
        [".measureText", ".font"]
        , source_code)
        
        return results[".measureText"] and results[".font"]