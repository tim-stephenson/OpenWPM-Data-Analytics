

from pathlib import Path
import logging
import sqlite3
from typing import Any, Dict, List, TextIO, Tuple, Type
from analyzers.analyzer import Analyzer


from analyzers.static_analyzers.canvas_1m_static import Canvas_1M_Static
from analyzers.static_analyzers.canvas_font_1m_static import Canvas_Font_1M_Static
from analyzers.static_analyzers.webrtc_1m_static import WebRTC_1M_Static
from analyzers.static_analyzers.webgl_static import WebGL_Static

from analyzers.dynamic_analyzers.canvas_1m_dynamic import Canvas_1M_Dynamic
from analyzers.dynamic_analyzers.canvas_font_1m_dynamic import Canvas_Font_1M_Dynamic
from analyzers.dynamic_analyzers.webrtc_1m_dynamic import WebRTC_1M_Dynamic
from analyzers.dynamic_analyzers.webgl_dynamic import WebGL_Dynamic

Canvas_1M_Static : Type[Analyzer] = Canvas_1M_Static
Canvas_Font_1M_Static : Type[Analyzer] = Canvas_Font_1M_Static
WebRTC_1M_Static : Type[Analyzer] = WebRTC_1M_Static
WebGL_Static : Type[Analyzer] = WebGL_Static

Canvas_1M_Dynamic : Type[Analyzer] = Canvas_1M_Dynamic
Canvas_Font_1M_Dynamic : Type[Analyzer] = Canvas_Font_1M_Dynamic
WebRTC_1M_Dynamic : Type[Analyzer] = WebRTC_1M_Dynamic
WebGL_Dynamic : Type[Analyzer] = WebGL_Dynamic


def GenerateLogger(filename : Path) -> logging.Logger:
    logger: logging.Logger = logging.getLogger('analysis')
    logger.setLevel(logging.DEBUG)

    formatter: logging.Formatter = logging.Formatter("%(asctime)s - (%(filename)s:%(lineno)d) - %(levelname)s\n%(message)s")
    

    ch: logging.StreamHandler[TextIO] = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh: logging.FileHandler = logging.FileHandler(filename, 'w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def run_all_analyzers(con : sqlite3.Connection, db : Any, logger : logging.Logger) -> Dict[str, List[Tuple[str,str]]]:
    results : Dict[str, List[Tuple[str,str]]] = dict()
    Analyzers : List[Type[Analyzer]] = [
        Canvas_1M_Static,Canvas_Font_1M_Static,WebRTC_1M_Static,WebGL_Static,
        Canvas_1M_Dynamic,Canvas_Font_1M_Dynamic,WebRTC_1M_Dynamic,WebGL_Dynamic
        ]
    for analyzer in Analyzers:
        a: Analyzer = analyzer(con,db,logger)
        results[a.analysis_name()] = a.analyze()
    return results

# def get_symmetric_difference()





