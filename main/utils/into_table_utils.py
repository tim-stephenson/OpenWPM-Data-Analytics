from sqlalchemy.engine import Engine
from sqlalchemy import MetaData
from typing import FrozenSet, List, Set, Tuple, Final
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

# Checks if a given table_name exists in a sql database
def table_exists(table_name : str, engine : Engine) -> bool:
    metadata_obj: MetaData = MetaData()
    metadata_obj.reflect(engine)
    return metadata_obj.tables.__contains__(table_name)


# Checks that a column exists in a given table.
def column_exists(table_name : str, column_name : str, engine : Engine) -> bool:
    metadata_obj: MetaData = MetaData()
    metadata_obj.reflect(engine)
    if metadata_obj.tables.__contains__(table_name):
        if metadata_obj.tables[table_name].c.__contains__(column_name):
            return True
    return False

# Taking the resulting fingerprinting analysis results, in a pandas dataframe as input, 
# saves that analysis data to the sql table, analysis_results
def dataframe_to_table(df : pandas.DataFrame,engine : Engine, table_name : str) -> None:
     df.to_sql(table_name,engine,if_exists="replace",index_label=["visit_id","script_url"] )

# Loads the fingerprinting analysis results from the analysis_results table into
# a pandas dataframe
def table_to_dataframe(engine : Engine, table_name : str) -> pandas.DataFrame:
    return pandas.read_sql_table(table_name,engine,index_col=["visit_id","script_url"])


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
