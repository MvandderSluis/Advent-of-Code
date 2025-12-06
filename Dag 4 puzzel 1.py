from typing import List


# 8 richtingen: horizontaal, verticaal en diagonaal
NEIGHBOR_DIRS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


def count_accessible_rolls(grid: List[str]) -> int:
    """
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


def test_example() -> None:
    """
    Controleer dat de gegeven voorbeeldkaart 13 oplevert.
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

    result = count_accessible_rolls(example_grid)
    expected = 13
    assert result == expected, f"Example failed: got {result}, expected {expected}"
    print(f"Test geslaagd: voorbeeld geeft {result} (verwacht {expected})")


def read_puzzle_input(filename: str) -> List[str]:
    """
    Lees de puzzelinvoer uit een tekstbestand.
    Lege regels worden genegeerd; regels worden gestript.
    """
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    # Optioneel: lege regels weghalen
    return [line for line in lines if line]


def main() -> None:
    # 1. Controleer eerst de testinput
    test_example()

    # 2. Lees de echte puzzelinvoer
    grid = read_puzzle_input("input_puzzel_dag4.txt")

    # 3. Bereken en print het aantal toegankelijke rollen
    result = count_accessible_rolls(grid)
    print("Aantal rollen dat door een vorkheftruck kan worden bereikt:", result)


if __name__ == "__main__":
    main()