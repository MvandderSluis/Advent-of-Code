def max_joltage_for_bank(line: str) -> int:
    """
    Bepaal de maximaal haalbare 2-cijferige joltage voor één bank.
    We mogen precies twee batterijen kiezen, in volgorde (positie i < j),
    en vormen dan het getal 10 * d_i + d_j.
    """
    digits = [int(c) for c in line.strip() if c.isdigit()]
    if len(digits) < 2:
        raise ValueError("Bank moet minimaal twee batterijen bevatten.")

    # We zoeken het paar (d1, d2) met i < j zó dat (d1, d2) lexicografisch maximaal is.
    # Dat is hetzelfde als het getal 10*d1 + d2 maximaliseren.
    best_pair = None          # (d1, d2)
    best_first = digits[0]    # grootste eerste cijfer dat we tot nu toe hebben gezien

    # Door de bank van links naar rechts te lopen, kan elke positie j tweede cijfer zijn.
    for j in range(1, len(digits)):
        d = digits[j]

        # Kandidatenpaar: (best_first, d) als tweede cijfer d.
        cand_pair = (best_first, d)
        if best_pair is None or cand_pair > best_pair:
            best_pair = cand_pair

        # Update best_first: we willen altijd het grootste cijfer tot nu toe als eerste positie
        if d > best_first:
            best_first = d

    d1, d2 = best_pair
    return 10 * d1 + d2


def total_output_joltage(lines) -> int:
    """Som van de maximale joltages per bank."""
    return sum(max_joltage_for_bank(line) for line in lines if line.strip())


def main():
    # --- 1. Controle met de testinput uit de opgave ---
    test_input = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]
    expected_test_total = 357  # 98 + 89 + 78 + 92

    test_total = total_output_joltage(test_input)
    assert test_total == expected_test_total, (
        f"Test faalt: verwacht {expected_test_total}, kreeg {test_total}"
    )
    print("test output:", test_total)

    # --- 2. Berekening voor de echte puzzelinput ---
    with open("input_puzzel_dag3.txt", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    result = total_output_joltage(lines)
    print("Totaal output joltage:", result)


if __name__ == "__main__":
    main()