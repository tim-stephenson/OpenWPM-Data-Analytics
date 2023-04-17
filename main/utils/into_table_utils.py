from sqlalchemy.engine import Engine
from sqlalchemy import MetaData
from typing import FrozenSet, List, Set, Tuple, Final
import pandas
from analyzers.analyzer import Analyzer
import numpy


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
    with engine.connect() as conn:
        return pandas.read_sql_table(table_name,conn,index_col=["visit_id","script_url"])


def analyzerObjects_to_dataframe(analyzer_objects : List[Analyzer]) -> pandas.DataFrame:
    domain : Set[Tuple[str,str]] = set()
    for analyzer in analyzer_objects:
        domain.update(analyzer.analysis_domain())
    analysis_names : List[str] = [analyzer.analysis_name() for analyzer in analyzer_objects]
    df: pandas.DataFrame = pandas.DataFrame(data=numpy.nan, index=pandas.MultiIndex.from_tuples(list(domain),names=['visit_id', 'script_url']), columns=analysis_names, dtype=float) #type: ignore
    for analyzer in analyzer_objects:
        for value in analyzer.analysis_domain():
            df.at[value, analyzer.analysis_name()] = 0 #type: ignore
        for value in analyzer.get_analysis_results():
            df.at[value, analyzer.analysis_name()] = 1 #type: ignore
    return df


# merge dataframe new and previous, which have the same rows but potentially different columns
# When a column is shared, the items in previous are discarded and the items in new are used
def merge_dataframes(new : pandas.DataFrame, previous : pandas.DataFrame) -> pandas.DataFrame:
    previous_filtered : pandas.DataFrame = previous.drop(columns=new.columns, errors='ignore')    
    join : pandas.DataFrame =  new.merge(previous_filtered, how='outer',on=None,left_index=True,right_index=True,validate="one_to_one") #type: ignore
    return join
