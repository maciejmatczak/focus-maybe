#!/usr/bin/env python

import argparse
from pathlib import Path
import os
import sys

import pcbnew

sys.path.append(str(Path(__file__).parent))
from common import path_type  # noqa


KICAD_MH_PRETTY = os.environ["KICAD_MH_PRETTY"]


def mh_add(pcb_path: str, footprint: str, x: float, y: float):
    mh_pretty = KICAD_MH_PRETTY

    board = pcbnew.LoadBoard(pcb_path)
    io = pcbnew.PCB_IO_KICAD_SEXPR()

    mod = io.FootprintLoad(mh_pretty, footprint)
    if not mod:
        print(f"{footprint} not found in {mh_pretty}")
        sys.exit(1)

    mod.SetPosition(
        pcbnew.VECTOR2I_MM(
            x,
            y,
        )
    )
    mod.Reference().SetText("generated")
    mod.Reference().SetVisible(False)
    mod.Value().SetVisible(False)

    print(f"=> Adding mh @ {x}; {y} mm")
    board.Add(mod)

    board.Save(board.GetFileName())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Places mounting holes on pcb, based on placement config. "
        "Expects a KICAD_MOUNTING_HOLE_PATH environment variable to be set "
        "(.env)."
    )
    parser.add_argument("pcb", type=path_type, help="PCB file path")
    parser.add_argument(
        "--footprint",
        type=str,
        default=None,
        help="Footprint name",
    )
    parser.add_argument(
        "-x",
        type=float,
        help="X coordinate in mm",
    )
    parser.add_argument(
        "-y",
        type=float,
        help="Y coordinate in mm",
    )

    args = parser.parse_args()

    mh_add(str(args.pcb), footprint=args.footprint, x=args.x, y=args.y)
