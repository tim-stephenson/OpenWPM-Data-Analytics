import importlib
import logging
from sqlalchemy.engine import Engine
from types import ModuleType
from typing import Any, Dict, List, Tuple, Type
from analyzers.analyzer import Analyzer
import analyzers


Canvas_1M_Static : Type[Analyzer] = analyzers.Canvas_1M_Static
Canvas_Basic_Static : Type[Analyzer] = analyzers.Canvas_Basic_Static
Canvas_Basic_Static_2 : Type[Analyzer] = analyzers.Canvas_Basic_Static_2
Canvas_Font_1M_Static : Type[Analyzer] = analyzers.Canvas_Font_1M_Static
WebRTC_1M_Static : Type[Analyzer] = analyzers.WebRTC_1M_Static
WebGL_Static : Type[Analyzer] = analyzers.WebGL_Static
Media_Queries_Static : Type[Analyzer] = analyzers.Media_Queries_Static
Navigator_Properties_Static : Type[Analyzer] = analyzers.Navigator_Properties_Static



Canvas_1M_Dynamic : Type[Analyzer] = analyzers.Canvas_1M_Dynamic
Canvas_Basic_Dynamic: Type[Analyzer] = analyzers.Canvas_Basic_Dynamic
Canvas1MDynamicND : Type[Analyzer] = analyzers.Canvas1MDynamicND
Canvas_Font_1M_Dynamic : Type[Analyzer] = analyzers.Canvas_Font_1M_Dynamic
WebRTC_1M_Dynamic : Type[Analyzer] = analyzers.WebRTC_1M_Dynamic
WebGL_Dynamic : Type[Analyzer] = analyzers.WebGL_Dynamic
Media_Queries_Dynamic : Type[Analyzer] = analyzers.Media_Queries_Dynamic
Navigator_Properties_Dynamic : Type[Analyzer] = analyzers.Navigator_Properties_Dynamic



Analyzers : List[Type[Analyzer]] = [
    Canvas_1M_Static,Canvas_Basic_Static,Canvas_Basic_Static_2,Canvas_Font_1M_Static,
    WebRTC_1M_Static,WebGL_Static,Media_Queries_Static,Navigator_Properties_Static,

    Canvas_1M_Dynamic,Canvas_Basic_Dynamic,Canvas1MDynamicND,Canvas_Font_1M_Dynamic,
    WebRTC_1M_Dynamic,WebGL_Dynamic,Media_Queries_Dynamic,Navigator_Properties_Dynamic
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






