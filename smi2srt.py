#!/usr/bin/env python3
import argparse
import logging
import os

from smi import SMI
from srt import SRT

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)


def main(args: argparse.Namespace):
    for subtitle_path in args.subtitle_list:
        assert subtitle_path.endswith(".smi")
        frame_list = SMI(subtitle_path).parse()

        new_filename = subtitle_path.replace(".smi", ".srt")

        SRT(frame_list, args.delay).write_to(new_filename)
        logging.info(f"{subtitle_path} -> {new_filename}")

        if args.clean:
            os.remove(subtitle_path)
            logging.info(f"{subtitle_path} removed")

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "subtitle_list",
        help="one or more smi file paths",
        nargs="+",
        type=str,
    )
    parser.add_argument(
        "-c",
        "--clean",
        help="remove the original smi files",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--delay",
        help="correct subtitle sync. set a float number in seconds",
        type=float,
        default=0,
    )

    args = parser.parse_args()
    main(args)
