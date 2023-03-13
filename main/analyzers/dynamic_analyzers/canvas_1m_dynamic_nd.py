import logging
import sqlite3
from typing import Any, List

from analyzers.dynamic_analyzer import Dynamic_Analyzer, parseArguments


def _nchars(s : str) -> int:
    """
    nchars(s) = the number of distinct characters in s.
    """
    return len(set(s))

def _minwh(b : List[Any], i : int) -> bool :
    """
    minwh(b, i) = true,  if (1) HTMLCanvasElement.height is not set in
                         b before row i, or (2) the last setting before
                         row i is to a value ≥ 16, and the same holds for
                         HTMLCanvasElement.width
                  false, otherwise.
    """
    # TODO: This verification of minimum dimensions presupposes that each
    # possible fingerprinting block accesses its own canvas.  Does that
    # match practice?

    height : int = -1
    width : int = -1

    for j in range(i, -1, -1):
        row = b[j]
        match (row['symbol'], row['operation']):
            case ('HTMLCanvasElement.height', 'set'):
                if height == -1 and row['value']:
                    height = float(row['value'])
            case ('HTMLCanvasElement.width', 'set'):
                if width == -1 and row['value']:
                    width = float(row['value'])

    return (width == -1 or width >= 16) and (height == -1 or height >= 16)

def _prev_color(b : List[Any], i : int) -> str :
    """
    _prev_color(b, i) = the color of the last call to
    `CanvasRenderingContext2D.fillStyle` before row i of b (None if there is no
    such call).
    """

    for j in range(i, -1, -1):
        if (b[j]['symbol'] == 'CanvasRenderingContext2D.fillStyle' and
                b[j]['operation'] == 'set'):
            return b[j]['value']

    return None


class Canvas1MDynamicND(Dynamic_Analyzer):

    def __init__(
            self,
            con : sqlite3.Connection,
            db : Any,
            logger : logging.Logger) -> None:
        Dynamic_Analyzer.__init__(self, con, db, logger)
        self._rows : List[Any] = []

    def fingerprinting_type(self) -> str:
        return "Canvas"

    def _partition_rows(self) -> List[List[Any]] :
        """
        partition_rows() = [rs₀, rs₁,...] where:
          - self._rows = rs₀ + rs₁ + ...
          - rs_i ends with a call to `toDataURL` and has no other calls to
            `toDataURL`.

        So partition_rows partitions the rows that were read into possible
        canvas fingerprinting blocks, where we think of each possible block as
        being a sequence of access that ends with a call to `toDataURL`.
        """
        blocks = [[]]

        # Create the partitions.  However, when finished, the last item in b
        # may be a block that does not end with `toDataURL`.
        for r in self._rows:
            blocks[-1].append(r)
            if r['symbol'] == 'HTMLCanvasElement.toDataURL':
                blocks.append([])

        # Delete the last block if it doesn't end with `toDataURL`.  That last
        # block could be empty.
        if (blocks[-1] != [] and 
                blocks[-1][-1]['symbol'] != 'HTMLCanvasElement.toDataURL'):
            blocks.pop()

        return blocks

    def _classify(self) -> bool:

        blocks : List[List[Any]]  = self._partition_rows()

        for b in blocks:
            # First make sure there is no `save`, `restore`, or
            # `addEventListenever` in this block.
            if len(list(filter(
                    lambda s: s in [
                        "HTMLCanvasElement.addEventListener",
                        "CanvasRenderingContext2D.save",
                        "CanvasRenderingContext2D.restore"],
                    [r['symbol'] for r in b]))) > 0:
                continue

            # Look for a call to `fillText` or `strokeText` with at least 10
            # characters.  The make sure it is preceeded by setting the canvas
            # dimensions to ≥ 16x16.
            for i in range(len(b)):
                if b[i]['symbol'] in [
                        'CanvasRenderingContext2D.fillText',
                        'CanvasRenderingContext2D.strokeText']:
                    args : List[Any] = parseArguments(b[i]['arguments'])
                    if args != [] and _nchars(args[0]) >= 10 and _minwh(b, i):
                        return True

            # Look for two calls to `fillText` or `strokeText` with two
            # different colors.
            for i in range(len(b)):
                if b[i]['symbol'] in [
                        'CanvasRenderingContext2D.fillText',
                        'CanvasRenderingContext2D.strokeText']:
                    color = _prev_color(b, i)
                    whok = _minwh(b, i)

                    for j in range(i+1, len(b)):
                        if b[j]['symbol'] in [
                                'CanvasRenderingContext2D.fillText',
                                'CanvasRenderingContext2D.strokeText']:
                            next_color = _prev_color(b, j)
                            next_whok = _minwh(b, j)

                            if color != next_color and whok and next_whok:
                                return True

                            break


        return False

    def _reset(self) -> None :
        self._rows = []
        return

    def _read_row(self, row : Any) -> None:
        self._rows.append(row)
        return

