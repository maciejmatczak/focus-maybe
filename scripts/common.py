import argparse
import os
from pathlib import Path


def path_type(string, exists=True, type_="file"):
    p = Path(string).resolve()

    if exists:
        if not p.exists():
            raise argparse.ArgumentTypeError(f"{string} is not existing path")

        if type_ == "file":
            if not p.is_file():
                raise argparse.ArgumentTypeError(f"{string} is not a file")
        else:
            if not p.is_dir():
                raise argparse.ArgumentTypeError(f"{string} is not a directory")

    return p
