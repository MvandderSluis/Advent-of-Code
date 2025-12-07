def parse_grid_from_string(s: str):
    """Neemt een multiline string en geeft een lijst van rijen terug."""
    lines = [line.rstrip("\n") for line in s.splitlines() if line.strip() != ""]
    return lines


def count_splits(grid):
    """
    Deel 1 (klassiek):
    Simuleer alle bundels en tel hoe vaak een bundel een splitter '^' raakt.
    """
    height = len(grid)
    if height == 0:
        return 0
    width = len(grid[0])

    # Zoek 'S'
    start = None
    for r, row in enumerate(grid):
        c = row.find('S')
        if c != -1:
            start = (r, c)
            break

    if start is None:
        raise ValueError("Geen 'S' gevonden in het rooster.")

    active = {start}
    splits = 0

    while active:
        new_active = set()

        for r, c in active:
            nr = r + 1
            if nr >= height:
                # bundel verlaat het manifold
                continue

            cell = grid[nr][c]

            if cell == '.' or cell == 'S':
                new_active.add((nr, c))
            elif cell == '^':
                splits += 1
                # links
                if c - 1 >= 0:
                    new_active.add((nr, c - 1))
                # rechts
                if c + 1 < width:
                    new_active.add((nr, c + 1))
            else:
                # Onbekende tekens behandelen als lege ruimte
                new_active.add((nr, c))

        active = new_active

    return splits


def count_timelines(grid):
    """
    Deel 2 (quantum / many-worlds):
    Tel hoeveel verschillende tijdlijnen één tachyon kan volgen, waarbij
    elke splitter '^' de tijdlijn in (maximaal) tweeën splitst.
    """
    height = len(grid)
    if height == 0:
        return 0
    width = len(grid[0])

    # Zoek 'S'
    start_row = None
    start_col = None
    for r, row in enumerate(grid):
        c = row.find('S')
        if c != -1:
            start_row = r
            start_col = c
            break

    if start_row is None:
        raise ValueError("Geen 'S' gevonden in het rooster.")

    # current[c] = aantal tijdlijnen op huidige rij 'row' op kolom c
    row = start_row
    current = [0] * width
    current[start_col] = 1

    finished = 0  # tijdlijnen die het manifold al hebben verlaten

    # Zolang we niet voorbij de laatste rij zijn
    while row < height - 1 and any(current):
        nr = row + 1
        new = [0] * width

        for c, count in enumerate(current):
            if count == 0:
                continue

            cell = grid[nr][c]

            if cell == '^':
                # Splitst naar links
                if c - 1 >= 0:
                    new[c - 1] += count
                else:
                    # valt links buiten het rooster → tijdlijn eindigt
                    finished += count

                # Splitst naar rechts
                if c + 1 < width:
                    new[c + 1] += count
                else:
                    # valt rechts buiten het rooster → tijdlijn eindigt
                    finished += count
            else:
                # Gewoon naar beneden
                new[c] += count

        current = new
        row = nr

    # Alles wat nog in 'current' zit, valt nu onder het rooster uit
    finished += sum(current)

    return finished


def run_test_example():
    """Controleer dat het voorbeeld uit de opgave 21 splits en 40 tijdlijnen geeft."""
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

    # Deel 1 test
    result_part1 = count_splits(example_grid)
    expected_part1 = 21
    if result_part1 != expected_part1:
        raise AssertionError(
            f"Test deel 1 faalde: verwacht {expected_part1}, kreeg {result_part1}."
        )
    print(f"Test deel 1 geslaagd: voorbeeld geeft {result_part1} splits.")

    # Deel 2 test
    result_part2 = count_timelines(example_grid)
    expected_part2 = 40
    if result_part2 != expected_part2:
        raise AssertionError(
            f"Test deel 2 faalde: verwacht {expected_part2}, kreeg {result_part2}."
        )
    print(f"Test deel 2 geslaagd: voorbeeld geeft {result_part2} tijdlijnen.")


def run_puzzle_input(filename: str = "input_puzzel_dag7.txt"):
    """Lees de echte puzzelinput en print oplossingen voor deel 1 en deel 2."""
    with open(filename, "r", encoding="utf-8") as f:
        grid = [line.rstrip("\n") for line in f if line.strip() != ""]

    part1 = count_splits(grid)
    part2 = count_timelines(grid)

    print(f"Aantal splits (deel 1) in {filename}: {part1}")
    print(f"Aantal tijdlijnen (deel 2) in {filename}: {part2}")


if __name__ == "__main__":
    # 1. Altijd eerst de voorbeeldtests
    run_test_example()

    # 2. Daarna rekenen op de echte input
    run_puzzle_input("input_puzzel_dag7.txt")