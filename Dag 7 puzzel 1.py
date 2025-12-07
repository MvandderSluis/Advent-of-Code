def parse_grid_from_string(s: str):
    """Neemt een multiline string en geeft een lijst van rijen terug."""
    lines = [line.rstrip("\n") for line in s.splitlines() if line.strip() != ""]
    # Eventuele lege regels boven/onder worden verwijderd
    return lines


def count_splits(grid):
    """
    Simuleer de tachyonbundels op het rooster 'grid' (lijst van strings)
    en geef het aantal splits (bezoeken aan '^') terug.
    """
    height = len(grid)
    if height == 0:
        return 0
    width = len(grid[0])

    # Zoek de startpositie 'S'
    start = None
    for r, row in enumerate(grid):
        c = row.find('S')
        if c != -1:
            start = (r, c)
            break

    if start is None:
        raise ValueError("Geen 'S' gevonden in het rooster.")

    active = {start}  # set van (rij, kolom)
    splits = 0

    while active:
        new_active = set()

        for r, c in active:
            nr = r + 1  # één stap naar beneden
            if nr >= height:
                # Bundel verlaat de manifold
                continue

            cell = grid[nr][c]

            if cell == '.':
                # Rechte doorgang naar beneden
                new_active.add((nr, c))
            elif cell == '^':
                # Bundel wordt gesplitst
                splits += 1

                # Nieuwe bundel links
                if c - 1 >= 0:
                    new_active.add((nr, c - 1))

                # Nieuwe bundel rechts
                if c + 1 < width:
                    new_active.add((nr, c + 1))
            else:
                # Alle andere karakters behandelen we als lege ruimte
                new_active.add((nr, c))

        active = new_active

    return splits


def run_test_example():
    """Controleer dat het voorbeeld uit de opgave 21 splits geeft."""
    example_str = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""
    example_grid = parse_grid_from_string(example_str)
    result = count_splits(example_grid)
    expected = 21
    if result != expected:
        raise AssertionError(
            f"Test faalde: verwacht {expected} splits, maar kreeg {result}."
        )
    print(f"Test geslaagd: voorbeeld geeft {result} splits.")


def run_puzzle_input(filename: str = "input_puzzel_dag7.txt"):
    """Lees de echte puzzelinput uit bestand en print het aantal splits."""
    with open(filename, "r", encoding="utf-8") as f:
        grid = [line.rstrip("\n") for line in f if line.strip() != ""]
    result = count_splits(grid)
    print(f"Aantal splits in {filename}: {result}")


if __name__ == "__main__":
    # 1. Eerst testen met het voorbeeld (moet 21 opleveren)
    run_test_example()

    # 2. Dan de echte puzzelinput doorrekenen
    run_puzzle_input("input_puzzel_dag7.txt")