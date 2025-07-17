#!/usr/bin/env python

import argparse
from pathlib import Path
import sys

import pcbnew

sys.path.append(str(Path(__file__).parent))
from common import path_type  # noqa


def mh_delete(pcb_path: str):
    board = pcbnew.LoadBoard(pcb_path)

    for m in board.GetFootprints():
        footprint_id = m.GetFPID().GetUniStringLibId()
        reference = m.Reference().GetText()

        # not being sure if there is better way to checkl what is a mounting hole?
        # holes placed by scripts does not have a ":" with a lib name in front
        if "MountingHole" in footprint_id and reference == "generated":
            print(
                f"=> Deleting {footprint_id} @ {[pcbnew.ToMM(e) for e in m.GetCenter()]} mm"
            )
            board.Delete(m)

    board.Save(board.GetFileName())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deletes all mounting holes")
    parser.add_argument("pcb", type=path_type, help="PCB file path")
    args = parser.parse_args()

    mh_delete(str(args.pcb))
