from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Region:
    w: int
    h: int
    counts: List[int]


SHAPE_HEADER_RE = re.compile(r"^\s*(\d+):\s*$")
REGION_LINE_RE = re.compile(r"^\s*(\d+)x(\d+):\s*(.*?)\s*$")


def parse_input(text: str) -> Tuple[Dict[int, int], List[Region]]:
    """
    Returns:
      shape_hash_counts: dict shape_index -> number of '#' cells
      regions: list of Region(w,h,counts)
    """
    lines = [ln.rstrip("\n").rstrip("\r") for ln in text.splitlines()]
    i = 0

    # ---- Parse shapes ----
    shape_hash_counts: Dict[int, int] = {}
    while i < len(lines):
        m = SHAPE_HEADER_RE.match(lines[i])
        if not m:
            break
        shape_idx = int(m.group(1))
        i += 1

        grid: List[str] = []
        while i < len(lines):
            ln = lines[i]
            if ln.strip() == "":
                break
            # stop if next shape or region starts
            if SHAPE_HEADER_RE.match(ln) or REGION_LINE_RE.match(ln):
                break
            grid.append(ln.strip())
            i += 1

        hash_count = sum(row.count("#") for row in grid)
        shape_hash_counts[shape_idx] = hash_count

        # skip blank lines
        while i < len(lines) and lines[i].strip() == "":
            i += 1

    # ---- Parse regions (scan all lines) ----
    regions: List[Region] = []
    for ln in lines:
        m = REGION_LINE_RE.match(ln)
        if not m:
            continue
        w = int(m.group(1))
        h = int(m.group(2))
        counts_str = m.group(3).strip()
        counts = [int(x) for x in counts_str.split()] if counts_str else []
        regions.append(Region(w=w, h=h, counts=counts))

    if not shape_hash_counts:
        raise ValueError("Geen shapes gevonden (verwacht blokken zoals '0:' gevolgd door #/. regels).")
    if not regions:
        raise ValueError("Geen regions gevonden (verwacht regels zoals '12x5: 1 0 2 ...').")

    return shape_hash_counts, regions


def region_can_fit(shape_hash_counts: Dict[int, int], region: Region) -> bool:
    area = region.w * region.h
    required = 0

    for idx, cnt in enumerate(region.counts):
        if cnt <= 0:
            continue
        if idx not in shape_hash_counts:
            # gevraagd shape-index bestaat niet -> onmogelijk
            return False
        required += cnt * shape_hash_counts[idx]

    return required <= area


def solve(text: str) -> int:
    shape_hash_counts, regions = parse_input(text)
    return sum(1 for r in regions if region_can_fit(shape_hash_counts, r))


def run_self_test() -> None:
    # Kleine test die het "alleen # telt"-principe controleert.
    # Shape 0 heeft 4 '#' (2x2 blok), shape 1 heeft 3 '#' (L-tromino).
    # Regio 2x2: 1x shape0 past exact (4<=4) -> True
    # Regio 2x2: 1x shape0 + 1x shape1 vereist 7>4 -> False
    test_input = """\
0:
##
##

1:
##
#.

2x2: 1 0
2x2: 1 1
"""
    ans = solve(test_input)
    assert ans == 1, f"Self-test faalt: verwacht 1, kreeg {ans}"


def main() -> None:
    run_self_test()
    path = Path("input_puzzel_dag12.txt")
    text = path.read_text(encoding="utf-8")
    ans = solve(text)
    print(ans)


if __name__ == "__main__":
    main()
