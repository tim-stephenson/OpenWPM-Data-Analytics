import importlib
import itertools
import logging
from sqlalchemy.engine import Engine
from types import ModuleType
from typing import Any, Dict, List, Set, Tuple, Type
from analyzers.analyzer import Analyzer

from analyzers.static_analyzers.canvas_1m_static import Canvas_1M_Static
from analyzers.static_analyzers.canvas_basic_static import Canvas_Basic_Static
from analyzers.static_analyzers.canvas_font_1m_static import Canvas_Font_1M_Static
from analyzers.static_analyzers.webrtc_1m_static import WebRTC_1M_Static
from analyzers.static_analyzers.webgl_static import WebGL_Static
from analyzers.static_analyzers.media_queries_static import Media_Queries_Static
from analyzers.static_analyzers.navigator_properties_static import Navigator_Properties_Static

from analyzers.dynamic_analyzers.canvas_1m_dynamic import Canvas_1M_Dynamic
from analyzers.dynamic_analyzers.canvas_basic_dynamic import Canvas_Basic_Dynamic
from analyzers.dynamic_analyzers.canvas_1m_dynamic_nd import Canvas1MDynamicND
from analyzers.dynamic_analyzers.canvas_font_1m_dynamic import Canvas_Font_1M_Dynamic
from analyzers.dynamic_analyzers.webrtc_1m_dynamic import WebRTC_1M_Dynamic
from analyzers.dynamic_analyzers.webgl_dynamic import WebGL_Dynamic
from analyzers.dynamic_analyzers.media_queries_dynamic import Media_Queries_Dynamic
from analyzers.dynamic_analyzers.navigator_properties_dynamic import Navigator_Properties_Dynamic


Canvas_1M_Static : Type[Analyzer] = Canvas_1M_Static
Canvas_Basic_Static : Type[Analyzer] = Canvas_Basic_Static
Canvas_Font_1M_Static : Type[Analyzer] = Canvas_Font_1M_Static
WebRTC_1M_Static : Type[Analyzer] = WebRTC_1M_Static
WebGL_Static : Type[Analyzer] = WebGL_Static
Media_Queries_Static : Type[Analyzer]  = Media_Queries_Static
Navigator_Properties_Static : Type[Analyzer]  = Navigator_Properties_Static



Canvas_1M_Dynamic : Type[Analyzer] = Canvas_1M_Dynamic
Canvas_Basic_Dynamic: Type[Analyzer] = Canvas_Basic_Dynamic
Canvas1MDynamicND : Type[Analyzer] = Canvas1MDynamicND
Canvas_Font_1M_Dynamic : Type[Analyzer] = Canvas_Font_1M_Dynamic
WebRTC_1M_Dynamic : Type[Analyzer] = WebRTC_1M_Dynamic
WebGL_Dynamic : Type[Analyzer] = WebGL_Dynamic
Media_Queries_Dynamic : Type[Analyzer]  = Media_Queries_Dynamic
Navigator_Properties_Dynamic : Type[Analyzer]  = Navigator_Properties_Dynamic



Analyzers : List[Type[Analyzer]] = [
    Canvas_1M_Static,Canvas_Basic_Static,Canvas_Font_1M_Static,WebRTC_1M_Static,WebGL_Static,Media_Queries_Static,Navigator_Properties_Static,
    Canvas_1M_Dynamic,Canvas_Basic_Dynamic,Canvas1MDynamicND,Canvas_Font_1M_Dynamic,WebRTC_1M_Dynamic,WebGL_Dynamic,Media_Queries_Dynamic,Navigator_Properties_Dynamic
]


def all_analyzers(engine : Engine, db : Any, logger : logging.Logger) -> List[Analyzer]:
    return [ analyzer(engine,db,logger) for analyzer in Analyzers ]


def analyzers_from_module_names(module_names : List[str], engine : Engine, db : Any, logger : logging.Logger)-> List[Analyzer]:
        mods_classes: List[Tuple[str, str, str]] = \
        [c.rpartition('.') for c in module_names]
        analyzer_objects : List[Analyzer] = []
        for mc in mods_classes:
            logger.info(mc)
            if mc[0] != '':
                m: ModuleType = importlib.import_module(mc[0])
                analyzer_objects.append(
                    getattr(m, mc[2])(engine, db, logger)
                )
            else:
                analyzer_objects.append(globals()[mc[2]](engine, db, logger))
        return analyzer_objects

def analyzers_from_class_names(class_names : List[str], engine : Engine, db : Any, logger : logging.Logger)-> List[Analyzer]:
    d : Dict[str, Type[Analyzer]] = { a.analysis_name() : a for a in Analyzers}
    for class_name in class_names:
        if class_name not in d:
            raise LookupError(f"no such analyzer object: {class_name}")
    return [ d[class_name](engine,db,logger) for class_name in class_names ]

def run_analyzers(analyzer_objects : List[Analyzer]) -> None:
    for analyzer  in analyzer_objects:
        analyzer.run_analysis()

def get_all_symmetric_differences(analyzer_objects : List[Analyzer], logger : logging.Logger) -> None:
    grouped_by_fingerprinting_type : Dict[str, List[Analyzer]] = dict()
    for analyzer in analyzer_objects:
        if analyzer.fingerprinting_type() in grouped_by_fingerprinting_type:
            grouped_by_fingerprinting_type[analyzer.fingerprinting_type()].append(analyzer)
        else:
            grouped_by_fingerprinting_type[analyzer.fingerprinting_type()] = [analyzer]
    for analyzer_subgroup in grouped_by_fingerprinting_type.values():
        for (analyzer1, analyzer2) in  itertools.combinations(analyzer_subgroup, 2):
            compare(analyzer1,analyzer2,logger)

def compare(analyzer1 : Analyzer, analyzer2 : Analyzer , logger : logging.Logger) -> None:
        intersection_classified : Set[Tuple[str,str]] = set(analyzer1.get_analysis_results()).intersection( analyzer2.get_analysis_results() )
        intersection_domain : Set[Tuple[str,str]] = set(analyzer1.analysis_domain()).intersection( analyzer2.analysis_domain() ) 
        
        logger.info(f"""
        Fingerprinting method: {analyzer1.fingerprinting_type()}, 
        classified by {analyzer1.analysis_name()} : {len(analyzer1.get_analysis_results())} / {analyzer1.analysis_domain_size()}
        classified by {analyzer2.analysis_name()} : {len(analyzer2.get_analysis_results())} / {analyzer2.analysis_domain_size()}
        intersection : {len(intersection_classified)} / {len(intersection_domain)}
        """)


def load_cache(analyzer_objects : List[Analyzer], cached_results : Dict[str, List[Tuple[str, str]]]) -> None:
    for analyzer in analyzer_objects:
        if analyzer.analysis_name() in cached_results:
            analyzer.set_analysis_results(cached_results[analyzer.analysis_name()])


def store_to_cache(analyzer_objects : List[Analyzer]) -> Dict[str, List[Tuple[str, str]]]:
    return {analyzer.analysis_name() : analyzer.get_analysis_results() for analyzer in analyzer_objects }






