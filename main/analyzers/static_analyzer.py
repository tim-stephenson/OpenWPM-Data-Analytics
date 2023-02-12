from abc import abstractmethod
import sqlite3
from typing import List, Set, Tuple

from analyzers.analyzer import Analyzer

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
    
    def analysis_domain(self) ->  List[ Tuple[str,str] ]:
        query_response: sqlite3.Cursor = self.con.execute("""
            SELECT DISTINCT visit_id,url
            FROM http_responses
            WHERE content_hash <> ""
        """)
        return query_response.fetchall()

    def _analyze(self) -> List[ Tuple[str,str] ]:
        content_hash_results : Set[bytes] = set()
        for key, value in self.db: 
            if self._analyze_one( str( value ,encoding="utf-8", errors='ignore') ): 
                self.logger.info(f"{key} \n\tUsing: {self.fingerprinting_type()} \n\tVia: {self.analysis_name()}")
                content_hash_results.add(key) 
        results : Set[Tuple[str,str]] = set()
        responses : sqlite3.Cursor = self.con.execute("""
            SELECT  visit_id, url, content_hash
            FROM http_responses 
            WHERE content_hash <> "" 
        """)
        responses.row_factory = sqlite3.Row # type: ignore
        for row in responses:
            if bytes( row["content_hash"], encoding="ascii" ) in content_hash_results:
                id : Tuple[str,str] = (row["visit_id"], row["url"] )
                results.add(id)
                self.logger.info(f"{id} \n\tUsing: {self.fingerprinting_type()} \n\tVia: {self.analysis_name()}")
        return list(results)


    @abstractmethod
    def _analyze_one(self,source_code : str) -> bool:
        """
        Given a source code (JavaScript) string
        return's True if doing the fingerprinting_type, False if not
        """
        pass




# def content_hash_to_javascript(db : Any, content_hash : bytes) -> str:
#     """
#     with a content_hash, returns the corresponding JavaScript source code from the 'leveldb'
#     """
#     return str( db.get(content_hash) ,encoding="utf-8", errors='ignore')

    

    