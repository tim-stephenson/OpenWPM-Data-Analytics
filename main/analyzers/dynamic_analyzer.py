
from abc import abstractmethod
import json
import sqlite3
from typing import Any, List, Tuple, Union

from main.analyzers.analyzer import Analyzer

"""
Abstract Base Class for all dynamic analyzers

See parent class 'Analyzer' for method descriptions
"""
class Dynamic_Analyzer(Analyzer):
    
    def analysis_domain_size(self) -> int:
        query_response: sqlite3.Cursor = self.con.execute("""
            SELECT COUNT(*)
            FROM (
            SELECT DISTINCT visit_id,script_url
            FROM JAVASCRIPT
            )
        """)
        n : int = query_response.fetchone()[0]
        return n

    def analyze(self) -> List[ Tuple[str,str] ]:
        results : List[Tuple[str,str]] = []
        ordered : sqlite3.Cursor = self.con.cursor().execute("""
            SELECT * 
            FROM javascript 
            PARTITION BY visit_id, script_url
        """) 
        ordered.row_factory = sqlite3.Row  # type: ignore
        previous : Union[ Tuple[str,str], None]  = None
        for row in ordered:
            id: Tuple[str, str]  = (row["visit_id"], row["script_url"] )
            if(previous == None):
                previous = id
            if( previous != id ):
                if self.__classify():
                    self.logger.info(f"{previous} \n\tUsing: {self.fingerprinting_type()} \n\tVia: {self.analysis_name()}")
                    results.append(previous)
                self.__reset()
                previous = id
            self.__read_row(row)
        return results
    
    @abstractmethod
    def __classify(self) -> bool:
        """
        Based on the row's read via '__read_row' since the last call to '__reset',
        return's True if doing the fingerprinting_type, False if not
        """
        pass

    @abstractmethod
    def __reset(self) -> bool:
        """
        reset any stored classification data from '__read_row' calls
        """
        pass

    @abstractmethod
    def __read_row(self, row : Any) -> None:
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
    