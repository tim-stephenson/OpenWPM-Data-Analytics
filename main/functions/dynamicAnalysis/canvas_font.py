import ast
from typing import Dict, Set
import pandas as pd
import logging      


def CanvasFont(df :  pd.DataFrame, logger : logging.Logger) -> bool:

    fonts : Set[str] = set()
    textMeasured : Dict[str, int] = dict()

    for row in df.itertuples():
        args = None
        try:
            if row.arguments is not None:
                args = ast.literal_eval(row.arguments)
        except ValueError:
            logger.info(f"Was unable to parse function arguments, row.arguments : {row.arguments}")
        try:
            match row.symbol:
                case 'CanvasRenderingContext2D.font':
                    if row.operation == 'set' and row.value:
                        fonts.add(row.value)
                case 'CanvasRenderingContext2D.measureText':
                    if row.operation == 'call' and args and len(args)==1:
                        textMeasured[args[0]] = 1 + (textMeasured[args[0]] if args[0] in textMeasured else 0)
        except Exception as e:
            logger.exception(f"Found Exception {e}, row: {row}")
    logger.info(f"fonts: {len(fonts)}   measureText calls : { max(textMeasured.values()) if len(textMeasured) > 0 else 0 } ")
    return len(fonts) >= 50 and (  ( max(textMeasured.values()) if len(textMeasured) > 0 else 0 ) >= 50 )