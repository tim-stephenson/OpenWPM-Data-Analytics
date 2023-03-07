from abc import abstractmethod
from sqlalchemy import text, CursorResult
from typing import List, Set, Tuple, Any

from analyzers.analyzer import Analyzer

"""
Abstract Base Class for all static analyzers

See parent class 'Analyzer' for method descriptions
"""
class Static_Analyzer(Analyzer):
    
    def analysis_domain_size(self) -> int:
        with self.engine.connect() as conn:
            query_response: CursorResult[Tuple[int]] = conn.execute(text("""
                SELECT COUNT(*)
                FROM (
                    SELECT DISTINCT visit_id,url
                    FROM http_responses
                    WHERE content_hash <> ""
                )
            """))
        return query_response.__next__().tuple()[0]
    
    def analysis_domain(self) ->  List[ Tuple[str,str] ]:
        with self.engine.connect() as conn:
            query_response: CursorResult[Tuple[str,str]] = conn.execute(text("""
                SELECT DISTINCT visit_id,url
                FROM http_responses
                WHERE content_hash <> ""
            """))
        return [ tuple(row) for row in query_response.fetchall()]

    def _analyze(self) -> List[ Tuple[str,str] ]:
        content_hash_results : Set[bytes] = set()
        for key, value in self.db: 
            if self._analyze_one( str( value ,encoding="utf-8", errors='ignore') ): 
                self.logger.info(f"{key} \n\tUsing: {self.fingerprinting_type()} \n\tVia: {self.analysis_name()}")
                content_hash_results.add(key) 
        with self.engine.connect() as conn:
            query_response: CursorResult[Any] = conn.execute(text(f"""
                SELECT visit_id, url
                FROM http_responses 
                WHERE content_hash IN ({", ".join([ '"' + str(content_hash,encoding="ascii") + '"' for content_hash in content_hash_results])})
            """))
        return [ tuple(row) for row in query_response.fetchall()]



    @abstractmethod
    def _analyze_one(self,source_code : str) -> bool:
        """
        Given a source code (JavaScript) string
        return's True if doing the fingerprinting_type, False if not
        """
        pass


    

    