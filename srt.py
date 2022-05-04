#!/usr/bin/env python3
import logging
from typing import List

from smi import SMI


class SRT:
    _logger = logging.getLogger("SRT")

    def __init__(self, data_from_SMI: List[SMI.Frame], delay: int = 0):
        self.data = data_from_SMI
        self.delay = delay
        return

    def serialize(self):
        for cnt, entry in enumerate(self.data, 1):
            yield "".join(
                [
                    str(cnt),
                    "\n",
                    self._frame_to_time(entry.begin_frame),
                    " --> ",
                    self._frame_to_time(entry.end_frame),
                    "\n",
                    entry.speech,
                    "\n\n",
                ]
            )

    def write_to(self, filename: str):
        with open(filename, "w+", encoding="utf-8") as f:
            for payload in self.serialize():
                f.write(payload)
        return

    def _frame_to_time(self, frame: int):
        def to_formatted(t: float):
            hour = int(t // 3600)
            t %= 3600

            minute = int(t // 60)
            t %= 60

            sec = int(t)
            millisec = round(1000 * (t - sec))
            ret = f"{hour:02d}:{minute:02d}:{sec:02d},{millisec:03d}"
            self._logger.debug(ret)
            return ret

        time_in_sec = (frame / 1000) + self.delay
        return to_formatted(time_in_sec)
