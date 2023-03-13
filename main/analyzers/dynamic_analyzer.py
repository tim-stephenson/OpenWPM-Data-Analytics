
from abc import abstractmethod
import json
from sqlalchemy import text, CursorResult
from typing import Any, List, Tuple, Union

from analyzers.analyzer import Analyzer

"""
Abstract Base Class for all dynamic analyzers

See parent class 'Analyzer' for method descriptions
"""
class Dynamic_Analyzer(Analyzer):
    
    def analysis_domain_size(self) -> int:
        with self.engine.connect() as conn:
            query_response: CursorResult[Tuple[int]] = conn.execute(text("""
                SELECT COUNT(*)
                FROM (
                    SELECT DISTINCT visit_id,script_url
                    FROM JAVASCRIPT
                )
            """))
        return query_response.__next__().tuple()[0]

    def analysis_domain(self) ->  List[ Tuple[str,str] ]:
        with self.engine.connect() as conn:
            query_response: CursorResult[Tuple[str,str]]= conn.execute(text("""
                SELECT DISTINCT visit_id,script_url
                FROM JAVASCRIPT
            """))
        return [ tuple(row) for row in query_response.fetchall()]

    def _analyze(self) -> List[ Tuple[str,str] ]:
        self._reset()
        results : List[Tuple[str,str]] = []
        with self.engine.connect() as conn:
            query_response: CursorResult[Any] = conn.execute(text("""
                SELECT visit_id, script_url, symbol, operation, value, arguments
                FROM javascript
                ORDER BY visit_id, script_url, event_ordinal ASC
            """))
        previous : Union[ Tuple[str,str], None]  = None
        for row in query_response.mappings():
            id: Tuple[str, str]  = (row["visit_id"], row["script_url"] )
            if(previous == None):
                previous = id
            elif( previous != id ):
                if self._classify():
                    self.logger.info(f"{previous} \n\tUsing: {self.fingerprinting_type()} \n\tVia: {self.analysis_name()}")
                    results.append(previous)
                self._reset()
                previous = id
            self._read_row(row)
        if previous != None and self._classify():
            self.logger.info(f"{previous} \n\tUsing: {self.fingerprinting_type()} \n\tVia: {self.analysis_name()}")
            results.append(previous)
        self._reset()
        return results
    
    @abstractmethod
    def _classify(self) -> bool:
        """
        Based on the row's read via '_read_row' since the last call to '_reset',
        return's True if doing the fingerprinting_type, False if not
        """
        pass

    @abstractmethod
    def _reset(self) -> None:
        """
        reset any stored classification data from '_read_row' calls
        """
        pass

    @abstractmethod
    def _read_row(self, row : Any) -> None:
        """
        read a row from the 'javascript' table, stores needed information to later classify
        """
        pass



def parseArguments(arguments : None | str) -> List[Any]:
    """
    Parse a string from the 'arguments' column of the 'javascript' SQL table
    This value represents the list of arguments passed a JavaScript function
    """
    if arguments is None:
        return []
    return json.loads(arguments)
    