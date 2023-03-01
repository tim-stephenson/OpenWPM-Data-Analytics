


import logging
import sqlite3
from typing import Final, List, Set, Tuple

import pandas
from analyzers.analyzer import Analyzer

TABLE_NAME : Final[str] = "analysis_results"

def table_exists(table_name : str, con : sqlite3.Connection) -> bool:
    query_response: sqlite3.Cursor = con.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
            )
        """,(table_name))
    return query_response.fetchone() is not None


def into_table(con : sqlite3.Connection,analyzer_objects : List[Analyzer], logger : logging.Logger) -> None:
    con.execute(f"""DROP TABLE IF EXISTS {TABLE_NAME}""")
    con.execute(f"""CREATE TABLE {TABLE_NAME}(
    visit_id INTEGER NOT NULL,
    script_url TEXT NOT NULL,
    { ", ".join([analyzer.analysis_name() + " TINY INT NOT NULL DEFAULT 0" for analyzer in analyzer_objects ])},
    PRIMARY KEY (visit_id, script_url)
    )"""
    )


def into_df(analyzer_objects : List[Analyzer], logger : logging.Logger) -> pandas.DataFrame:
    domain : Set[Tuple[str,str]] = set()
    for analyzer in analyzer_objects:
        domain.update(analyzer.analysis_domain())
    analysis_names : List[str] = [analyzer.analysis_name() for analyzer in analyzer_objects]
    df: pandas.DataFrame = pandas.DataFrame(data=False,  index=pandas.MultiIndex.from_tuples(list(domain)), columns=analysis_names, dtype=bool) #type: ignore
    for analyzer in analyzer_objects:
        for value in analyzer.get_analysis_results():
            df[analyzer.analysis_name()].loc[value] = True #type: ignore
    return df