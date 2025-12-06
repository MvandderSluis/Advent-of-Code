def max_joltage_for_bank(line: str, k: int = 12) -> int:
    """
    Kies precies k batterijen (cijfers) in volgorde (subsequentie) zodat
    het gevormde getal maximaal is.

    Dit is: vind de lexicografisch grootste subsequentie van lengte k.
    """
    digits = [int(c) for c in line.strip() if c.isdigit()]
    n = len(digits)
    if n < k:
        raise ValueError(f"Bank heeft te weinig batterijen ({n}) voor k={k}.")

    removals = n - k   # zoveel cijfers moeten we in totaal weggooien
    stack = []

    for d in digits:
        # Zolang we nog cijfers mogen weggooien en het laatste cijfer in de stack
        # kleiner is dan het huidige cijfer, gooien we dat kleinere cijfer weg.
        while removals > 0 and stack and stack[-1] < d:
            stack.pop()
            removals -= 1
        stack.append(d)

    # Als we nog cijfers over hebben om weg te gooien, haal ze van het eind af.
    if removals > 0:
        stack = stack[:-removals]

    # Stack heeft nu precies lengte k en is de maximaal mogelijke subsequentie.
    result_str = "".join(str(x) for x in stack[:k])
    return int(result_str)


def total_output_joltage(lines, k: int = 12) -> int:
    """Som van de maximale k-cijferige joltages per bank."""
    return sum(max_joltage_for_bank(line, k) for line in lines if line.strip())


def main():
    # --- 1. Controle met de testinput uit de opgave ---
    test_input = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]
    expected_test_total = 3121910778619  # uit de tekst

    test_total = total_output_joltage(test_input, k=12)
    assert test_total == expected_test_total, (
        f"Test faalt: verwacht {expected_test_total}, kreeg {test_total}"
    )

    # --- 2. Berekening voor de echte puzzelinput ---
    with open("input_puzzel_dag3.txt", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    result = total_output_joltage(lines, k=12)
    print("Nieuw totaal output joltage:", result)


if __name__ == "__main__":
    main()