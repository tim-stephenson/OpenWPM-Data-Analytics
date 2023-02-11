from typing import Dict
from analyzers.static_analyzer import Static_Analyzer
from analyzers.static_analyzers.grep_utils import grepForKeywords


class WebGL_Static(Static_Analyzer):

    def fingerprinting_type(self) -> str:
        return "WebGL"
    
    def _analyze_one(self,source_code : str) -> bool:
        results: Dict[str, bool] = grepForKeywords(
        [".getParameter"]
        , source_code)
        
        return results[".getParameter"]