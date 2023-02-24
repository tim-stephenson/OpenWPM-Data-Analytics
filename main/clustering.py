from typing import List, Set, Tuple, Dict
from sklearn.cluster import KMeans
from analyzers.analyzer import Analyzer
import logging
import pandas
import json

def clusters(analyzer_objects : List[Analyzer], logger : logging.Logger) -> None:
    domain : Set[Tuple[str,str]] = set()
    for analyzer in analyzer_objects:
        domain.update(analyzer.analysis_domain())
    analysis_names : List[str] = [analyzer.analysis_name() for analyzer in analyzer_objects]
    df: pandas.DataFrame = pandas.DataFrame(data=False,  index=pandas.MultiIndex.from_tuples(list(domain)), columns=analysis_names, dtype=bool) #type: ignore
    for analyzer in analyzer_objects:
        for value in analyzer.get_analysis_results():
            df[analyzer.analysis_name()].loc[value] = True #type: ignore
    logger.info(str(df))
    model: KMeans = KMeans(algorithm="elkan",n_clusters=20, random_state=0,max_iter=1000, n_init=10) #type: ignore
    fit: KMeans = model.fit(df) #type: ignore

    logger.info(fit.cluster_centers_) #type: ignore
    logger.info(fit.labels_) #type: ignore
    logger.info(fit.inertia_ ) #type: ignore
    logger.info(fit.n_iter_ ) #type: ignore
    logger.info(fit.n_features_in_ ) #type: ignore
    logger.info(fit.feature_names_in_ ) #type: ignore
    logger.info(f"len(df) : {len(df)}")
    logger.info(f"len(domain) : {len(domain)}")
    logger.info(f"Average inertia: {fit.inertia_ / len(df)}") #type: ignore

    # counts[idx] = number of (visit_id,script_url) pairs in the idx's cluster group
    counts : List[int] = [ 0 for _ in range(len(fit.cluster_centers_)) ] #type: ignore
    for l in fit.labels_: #type: ignore
        counts[l] += 1 #type: ignore
    logger.info(f"counts: {counts}")

    results : List[ Tuple[ Dict[ str, float ], int ] ] = []
    for idx, center in enumerate(fit.cluster_centers_): #type: ignore
        results.append( ( {  fit.feature_names_in_[i] : center[i] for i in range(len(center))  }, counts[idx] ) ) #type: ignore
    
    results.sort(key = lambda v : v[1])
    logger.info(json.dumps(results,  indent=4))