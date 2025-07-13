from pathlib import Path


BUILD = Path(__file__).resolve().parent / "build"

BOARDS = [
    "base_top/base_top.kicad_pcb",
]


def task_plot():
    for board in BOARDS:
        board_name = Path(board).parts[0]
        yield {
            "name": f"plot {board_name}",
            "actions": [
                f"kicad-cli pcb export gerbers --output build/fab/{board_name} --layers F.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts "
                f"{board}",
                f"kicad-cli pcb export drill --output build/fab/{board_name} {board}",
            ],
        }
