from typing import List, Tuple

# 8 richtingen: horizontaal, verticaal en diagonaal
NEIGHBOR_DIRS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


def count_accessible_rolls(grid: List[str]) -> int:
    """
    Deel 1:
    Tel het aantal rollen (@) die minder dan 4 @-buren hebben
    in de 8 aangrenzende posities.
    """
    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])

    total = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "@":
                continue

            neighbor_count = 0
            for dr, dc in NEIGHBOR_DIRS:
                rr = r + dr
                cc = c + dc
                if 0 <= rr < rows and 0 <= cc < cols:
                    if grid[rr][cc] == "@":
                        neighbor_count += 1

            if neighbor_count < 4:
                total += 1

    return total


def simulate_removals(grid: List[str]) -> Tuple[int, List[str]]:
    """
    Deel 2:
    Herhaal:
      - zoek alle rollen (@) met minder dan 4 @-buren
      - verwijder ze allemaal tegelijk
    totdat er geen rollen meer verwijderd kunnen worden.
    Geef terug:
      - totaal aantal verwijderde rollen
      - het eindraster als lijst van strings
    """
    if not grid:
        return 0, grid

    rows = len(grid)
    cols = len(grid[0])

    # Werk met een mutabele kopie (lijst van lijsten met chars)
    current = [list(row) for row in grid]

    total_removed = 0

    while True:
        to_remove = []

        # Zoek alle verwijderbare rollen in de huidige toestand
        for r in range(rows):
            for c in range(cols):
                if current[r][c] != "@":
                    continue

                neighbor_count = 0
                for dr, dc in NEIGHBOR_DIRS:
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < rows and 0 <= cc < cols:
                        if current[rr][cc] == "@":
                            neighbor_count += 1

                if neighbor_count < 4:
                    to_remove.append((r, c))

        # Als er niets meer verwijderd kan worden: klaar
        if not to_remove:
            break

        # Verwijder alles van deze ronde in één keer
        for r, c in to_remove:
            current[r][c] = "."

        total_removed += len(to_remove)

    # Zet het eindraster terug naar lijst van strings
    final_grid = ["".join(row) for row in current]
    return total_removed, final_grid


def test_example() -> None:
    """
    Controleer dat de gegeven voorbeeldkaart:
      - 13 toegankelijke rollen geeft voor deel 1
      - 43 totaal verwijderde rollen geeft voor deel 2
    """
    example_grid = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]

    # Deel 1 test
    part1_result = count_accessible_rolls(example_grid)
    expected_part1 = 13
    assert part1_result == expected_part1, (
        f"Example deel 1 faalt: kreeg {part1_result}, verwacht {expected_part1}"
    )

    # Deel 2 test
    total_removed, _ = simulate_removals(example_grid)
    expected_removed = 43
    assert total_removed == expected_removed, (
        f"Example deel 2 faalt: kreeg {total_removed}, verwacht {expected_removed}"
    )

    print(
        f"Tests geslaagd: deel 1 = {part1_result} (13), "
        f"deel 2 totaal verwijderd = {total_removed} (43)"
    )


def read_puzzle_input(filename: str) -> List[str]:
    """
    Lees de puzzelinvoer uit een tekstbestand.
    Lege regels worden genegeerd; regels worden gestript.
    """
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    return [line for line in lines if line]


def main() -> None:
    # 1. Controleer eerst de testinput (voorbeeld)
    test_example()

    # 2. Lees de echte puzzelinvoer
    grid = read_puzzle_input("input_puzzel_dag4.txt")

    # 3. Deel 1: aantal direct toegankelijke rollen
    part1 = count_accessible_rolls(grid)
    print("Deel 1 - aantal direct toegankelijke rollen:", part1)

    # 4. Deel 2: totaal aantal verwijderde rollen na herhaald verwijderen
    total_removed, _ = simulate_removals(grid)
    print("Deel 2 - totaal aantal verwijderde rollen:", total_removed)


if __name__ == "__main__":
    main()