from typing import Set
import pandas as pd
import ast
import logging      


def Canvas(df :  pd.DataFrame, logger : logging.Logger) -> bool:
    # condition 1:
    heightORwidthTooSmall : bool = False
    # condition 2:
    colors : Set[str] = set()
    characters : Set[str] = set()
    # condition 3:
    ProductiveCalls : bool = False
    #Condition 4:
    Extraction : bool = False
    for row in df.itertuples():
        args = None
        try:
            if row.arguments is not None:
                args = ast.literal_eval(row.arguments)
        except ValueError:
            logger.info(f"Was unable to parse function arguments, row.arguments : {row.arguments}")
        try:
            match row.symbol:
                case 'HTMLCanvasElement.height':
                    if row.operation == 'set' and row.value and float(row.value) < 16:
                        heightORwidthTooSmall = True
                case 'HTMLCanvasElement.width':
                    if row.operation == 'set' and row.value and float(row.value) < 16:
                        heightORwidthTooSmall = True
                case 'CanvasRenderingContext2D.fillText':
                    if args is not None:
                        for char in args[0]:
                            characters.add(char)
                case 'CanvasRenderingContext2D.fillStyle':
                    if row.operation == 'set' and row.value:
                        colors.add(row.value)
                case 'HTMLCanvasElement.toDataURL':
                    Extraction = True
                case 'CanvasRenderingContext2D.getImageData':
                    if args is not None:
                        if abs( args[2] ) >= 16 and abs( args[3] ) >= 16:
                            Extraction = True
                case 'HTMLCanvasElement.addEventListener':
                    ProductiveCalls = True
                case 'CanvasRenderingContext2D.save':
                    ProductiveCalls = True
                case 'CanvasRenderingContext2D.restore':
                    ProductiveCalls = True
        except Exception as e:
            logger.exception(f"Found Exception {e}, row: {row}")

    #       condition 1                    condition 2                                   condition 3            condition 4
    return (not heightORwidthTooSmall) and ( len(colors) > 2 or len(characters) > 10) and (not ProductiveCalls) and Extraction