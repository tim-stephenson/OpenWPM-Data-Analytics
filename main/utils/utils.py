from pathlib import Path
import logging
from typing import Iterable, TextIO, Callable
from io import TextIOBase, StringIO


def GenerateLogger(filename : Path) -> logging.Logger:
    logger: logging.Logger = logging.getLogger('analysis')
    logger.setLevel(logging.DEBUG)

    formatter: logging.Formatter = logging.Formatter("%(asctime)s - (%(filename)s:%(lineno)d) - %(levelname)s\n%(message)s")
    formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    formatter.default_msec_format = '%s.%03d'

    ch: logging.StreamHandler[TextIO] = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh: logging.FileHandler = logging.FileHandler(filename, 'w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

# class LoggerInputStream(TextIOBase):

#     def __init__(self, writer : Callable[[str] ,None] ) -> None:
#         self.__writer: Callable[[str] ,None]  = writer
    
#     def fileno(self) -> int:
#         raise OSError

#     def readable(self) -> bool:
#         return False
    
#     def writable(self) -> bool:
#         return True
    
#     def seekable(self) -> bool:
#         return False
    
#     def writelines(self, lines: Iterable[str]) -> None:
#         for line in lines:
#             self.__writer(line)
        
#     def write(self, s: str) -> int:
#         self.__writer(s)
#         return -1
    
#     @property
#     def encoding(self) -> str:
#         return "utf-8"

class LoggerInputStream(StringIO):
   
    def __init__(self, writer : Callable[[str] ,None] ) -> None:
        self.__writer : Callable[[str] ,None]  = writer
        super().__init__("","\n")
    
    def fileno(self) -> int:
        raise OSError

    def writelines(self, lines: Iterable[str]) -> None:
        for line in lines:
            self.__writer(line)
        
    def write(self, s: str) -> int:
        self.__writer(s)
        return len(s)
    
    

    
