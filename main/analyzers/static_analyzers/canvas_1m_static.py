from typing import Dict
from analyzers.static_analyzer import Static_Analyzer
from analyzers.static_analyzers.grep_utils import grepForKeywords


class Canvas_1M_Static(Static_Analyzer):

    def fingerprinting_type(self) -> str:
        return "Canvas"
    
    def _analyze_one(self,source_code : str) -> bool:
        results: Dict[str, bool] = grepForKeywords(
        [".toDataURL", ".getImageData", ".addEventListener", ".save", ".restore", ".fillStyle", ".fillText", ".width", ".height"]
        , source_code)

        characters : bool = results[".fillText"]
        colors : bool = results[".fillStyle"]
        Extraction : bool = results[".toDataURL"] or results[".getImageData"] 
        return characters and colors and Extraction