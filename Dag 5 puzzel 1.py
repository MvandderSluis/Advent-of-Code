def parse_ranges(ranges_str: str):
    """Zet tekst met regels 'start-end' om naar een lijst (start, end)-tuples."""
    ranges = []
    for line in ranges_str.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        start_str, end_str = line.split("-")
        ranges.append((int(start_str), int(end_str)))
    return ranges


def count_fresh_ids(ranges, ids_str: str) -> int:
    """Tel hoeveel IDs in ids_str in minstens één range vallen."""
    fresh_count = 0
    for line in ids_str.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        x = int(line)
        # Check of x in één van de ranges valt
        if any(start <= x <= end for (start, end) in ranges):
            fresh_count += 1
    return fresh_count


def main():
    # 1. Test met de voorbeeldinput
    example_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
    ranges_part, ids_part = example_input.split("\n\n")
    ranges_example = parse_ranges(ranges_part)
    example_result = count_fresh_ids(ranges_example, ids_part)
    print("Testresultaat (moet 3 zijn):", example_result)

    # 2. Nu de echte puzzelinput uit bestand
    filename = "input_puzzel_dag5.txt"
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Splitsen op de eerste lege regel
    parts = content.split("\n\n", 1)
    if len(parts) != 2:
        raise ValueError(
            f"Invoerbestand '{filename}' heeft niet het verwachte formaat "
            "(er moet één lege regel tussen ranges en IDs staan)."
        )

    ranges_part, ids_part = parts
    ranges_puzzle = parse_ranges(ranges_part)
    puzzle_result = count_fresh_ids(ranges_puzzle, ids_part)

    print("Aantal verse ingredient IDs in de puzzelinput:", puzzle_result)


if __name__ == "__main__":
    main()