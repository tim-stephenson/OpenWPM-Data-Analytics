import sqlite3
from typing import Any, FrozenSet, List, Set, Tuple, Final

import pandas
from analyzers.analyzer import Analyzer

PROTECTED_TABLE_NAMES : Final[FrozenSet[str]] = frozenset([
"task",
"crawl",
"site_visits",
"crawl_history",
"http_requests",
"http_responses",
"http_redirects",
"javascript",
"javascript_cookies",
"navigations",
"callstacks",
"incomplete_visits",
"dns_responses"])

# Checks if a given table_name exists in a sqlite3 database
def table_exists(table_name : str, con : sqlite3.Connection) -> bool:
    query_response: sqlite3.Cursor = con.execute("""
            SELECT name 
            FROM sqlite_master
            WHERE type='table' AND name=?
        """,[table_name])
    result : Any = query_response.fetchone()
    return result is not None and result[0] == table_name

# Taking the resulting fingerprinting analysis results, in a pandas dataframe as input, 
# saves that analysis data to the sqlite3 table, analysis_results
def dataframe_to_table(df : pandas.DataFrame,con : sqlite3.Connection, table_name : str) -> None:
     df.to_sql(table_name,con,if_exists="replace",index_label=["visit_id","script_url"] )

# Loads the fingerprinting analysis results from the analysis_results table into
# a pandas dataframe
def table_to_dataframe(con : sqlite3.Connection, table_name : str) -> pandas.DataFrame:
    return pandas.read_sql(f"""
    SELECT *
    FROM {table_name}
    """,con,["visit_id","script_url"])


def analyzerObjects_to_dataframe(analyzer_objects : List[Analyzer]) -> pandas.DataFrame:
    domain : Set[Tuple[str,str]] = set()
    for analyzer in analyzer_objects:
        domain.update(analyzer.analysis_domain())
    analysis_names : List[str] = [analyzer.analysis_name() for analyzer in analyzer_objects]
    df: pandas.DataFrame = pandas.DataFrame(data=False,  index=pandas.MultiIndex.from_tuples(list(domain)), columns=analysis_names, dtype=bool) #type: ignore
    for analyzer in analyzer_objects:
        for value in analyzer.get_analysis_results():
            df[analyzer.analysis_name()].loc[value] = True #type: ignore
    return df

def dataframe_to_analyzerObjects(analyzer_objects : List[Analyzer], df : pandas.DataFrame) -> None:
    for analyzer in analyzer_objects:
        lst : List[Tuple[str,str]] = []
        for index, value in df[analyzer.analysis_name()].items(): #type: ignore
            if value:
                lst.append(index) #type: ignore
        analyzer.set_analysis_results(lst)