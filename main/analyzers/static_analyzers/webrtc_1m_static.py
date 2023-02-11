from typing import Dict
from analyzers.static_analyzer import Static_Analyzer
from analyzers.static_analyzers.grep_utils import grepForKeywords


class WebRTC_1M_Static(Static_Analyzer):

    def fingerprinting_type(self) -> str:
        return "WebRTC"
    
    def _analyze_one(self,source_code : str) -> bool:
        results: Dict[str, bool] = grepForKeywords(
        [".createDataChannel", ".createOffer", ".onicecandidate"]
        , source_code)
        
        return results[".createDataChannel"] and results[".createOffer"] and results[".onicecandidate"]