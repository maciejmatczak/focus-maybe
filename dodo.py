import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
KICAD_PYTHON = os.environ["KICAD_PYTHON"]
ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
PARAMETERS = json.loads((ROOT / "parameters.json").read_text())

BOARDS = {"base_top": {}, "pcb": {}}


def task_plot_all():
    for board, data in BOARDS.items():
        yield {
            "name": f"plot {board}",
            "actions": [
                f"kicad-cli pcb export gerbers --output build/fab/{board} --layers F.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts "
                f"{board}",
                f"kicad-cli pcb export drill --output build/fab/{board} {board}.kicad_pcb",
            ],
        }


def task_reload_holes():
    base_mh = PARAMETERS["base_mh"]
    footprint = base_mh["footprint"]
    holes = base_mh["holes"]

    def check_board(board):
        print(f"Checking board: {board}")
        if not board:
            raise ValueError("Board name cannot be empty.")

    actions = [
        check_board,
        f'"{KICAD_PYTHON}" ./scripts/mh_delete_all.py %(board)s/%(board)s.kicad_pcb',
    ]
    for hole in holes:
        x = hole["x"]
        y = hole["y"]
        actions.append(
            f'"{KICAD_PYTHON}" ./scripts/mh_add.py %(board)s/%(board)s.kicad_pcb --footprint {footprint} -x {x} -y {y}'
        )

    return {"pos_arg": "board", "actions": actions}
