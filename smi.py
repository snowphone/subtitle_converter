import logging
import re
from dataclasses import astuple, dataclass
from typing import List


class SMI:
    @dataclass
    class Frame:
        begin_frame: int  # frame unit: ms
        end_frame: int  # frame unit: ms
        speech: str

        def __iter__(self):
            return (it for it in astuple(self))

    _logger = logging.getLogger("SMI")

    def __init__(self, filename: str):
        self.filename = filename
        encoding = "utf-8" if self.is_utf8(filename) else "euc-kr"
        self._logger.info(f"{filename=}, {encoding=}")

        with open(
            filename,
            encoding=encoding,
            errors="ignore",
        ) as f:
            self.lines = f.readlines()
        return

    @staticmethod
    def is_utf8(filename: str):
        with open(filename, "rb") as f:
            data = f.read()
        try:
            data.decode("UTF-8")
        except UnicodeDecodeError:
            return False
        else:
            return True

    def parse(self):
        """
        return a list of (begin_frame, end_frame, speech)
        frame unit: ms
        """

        ret: List[SMI.Frame] = []
        idx = 0
        while True:
            try:
                begin_idx, begin_frame = self._find_sync(idx)
                end_idx, end_frame = self._find_sync(begin_idx + 1)
            except EOFError:
                break

            speech = [
                line
                for line in (
                    self._get_pure_speech(line)
                    for line in self.lines[begin_idx:end_idx]
                )
                if line
            ]

            if speech:
                data = self.Frame(begin_frame, end_frame, "\n".join(speech))
                ret.append(data)

                self._logger.debug(data)

            idx = end_idx

        return ret

    def _get_pure_speech(self, line: str):
        useless_pattern = re.compile(r"(<.*?>)|(&nbsp;)|(\n)")
        return useless_pattern.sub("", line)

    def _find_sync(self, start_from):
        """return (index, frame)"""
        start_pattern = re.compile(r"(?<=<SYNC Start=)\d+(?=><P Class=KRCC>)")
        size = len(self.lines)
        for i in range(start_from, size):
            result = start_pattern.search(self.lines[i])
            if not result:
                continue
            self._logger.debug(f"{i=}, {result.group()=}")
            return i, int(result.group())
        raise EOFError

    # end of SMI
