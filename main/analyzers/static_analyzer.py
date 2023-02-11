from abc import abstractmethod
import sqlite3
from typing import List, Tuple

from main.analyzers.analyzer import Analyzer

"""
Abstract Base Class for all static analyzers

See parent class 'Analyzer' for method descriptions
"""
class Static_Analyzer(Analyzer):
    
    def analysis_domain_size(self) -> int:
        query_response: sqlite3.Cursor = self.con.execute("""
            SELECT COUNT(*)
            FROM (
            SELECT DISTINCT visit_id,url
            FROM http_responses
            WHERE content_hash <> ""
            )
        """)
        n : int = query_response.fetchone()[0]
        return n

    def analyze(self) -> List[ Tuple[str,str] ]:
        results : List[Tuple[str,str]] = []
        responses : sqlite3.Cursor = self.con.cursor().execute("""
            SELECT  visit_id, url, content_hash
            FROM http_responses 
            WHERE content_hash <> "" 
        """)
        responses.row_factory = sqlite3.Row # type: ignore
        for row in responses:
            if self.__analyze_one(bytes( row["content_hash"], encoding="ascii" )):
                id : Tuple[str,str] = (row["visit_id"], row["url"] )
                results.append(id)
                self.logger.info(f"{id} \n\tUsing: {self.fingerprinting_type()} \n\tVia: {self.analysis_name()}")
        return results


    @abstractmethod
    def __analyze_one(self,content_hash : bytes) -> bool:
        """
        Given a a content_hash, which is a key in the 'leveldb'
        return's True if doing the fingerprinting_type, False if not
        """
        pass
    
    def __content_hash_to_javascript(self, content_hash : bytes) -> str: # type: ignore
        """
        with a content_hash, returns the corresponding JavaScript source code from the 'leveldb'
        """
        return str( self.db.get(content_hash) ,encoding="utf-8", errors='ignore')

    

    