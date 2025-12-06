# dag6_cephalopod_math_deel2.py

TEST_INPUT = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

EXPECTED_TEST_TOTAL = 3263827


def parse_worksheet(lines):
    """
    Zet de ruwe tekstregels om in een lijst van problemen.
    Deel 2-regels:
    - Eén probleem = één blok kolommen tussen volledig lege kolommen.
    - Onderaan staat in één van de kolommen van het blok de operator (+ of *).
    - Boven die onderste regel vormen de kolommen de getallen.
      * Elke kolom is precies één getal.
      * De bovenste rij is het meest significante cijfer.
      * De onderste rij (net boven de operator) is het minst significante cijfer.
    - Getallen worden per probleem RECHTS-NAAR-LINKS gelezen (dus rechter kolom is het eerste getal).
    """
    # Maak een rechthoekig grid: alle regels even lang, spaties behouden.
    width = max(len(line) for line in lines)
    grid = [line.rstrip("\n").ljust(width) for line in lines]

    nrows = len(grid)
    ncols = width

    # Bepaal per kolom of er ergens een niet-spatie staat.
    content_cols = []
    for c in range(ncols):
        has_content = any(grid[r][c] != " " for r in range(nrows))
        content_cols.append(has_content)

    # Groepeer opeenvolgende content-kolommen tot segmenten.
    segments = []
    c = 0
    while c < ncols:
        if not content_cols[c]:
            c += 1
            continue
        start = c
        while c < ncols and content_cols[c]:
            c += 1
        end = c - 1
        segments.append((start, end))

    problems = []
    for start, end in segments:
        # Onderste regel (operator-regel) binnen dit segment.
        bottom_slice = grid[-1][start : end + 1]
        op_char = None

        for ch in bottom_slice:
            if ch in "+*":
                if op_char is not None and ch != op_char:
                    raise ValueError("Meer dan één (verschillende) operator in een probleemsegment.")
                op_char = ch

        if op_char is None:
            # Geen operator = geen geldig probleem.
            continue

        nums = []
        # Kolommen worden RECHTS-NAAR-LINKS gelezen.
        for c in range(end, start - 1, -1):
            digits = []
            # Alleen rijen boven de operator; onderste rij is operator-regel.
            for r in range(nrows - 1):
                ch = grid[r][c]
                if ch != " " and ch.isdigit():
                    digits.append(ch)

            if digits:
                # Bovenaan is meest significante cijfer, dus gewoon joinen in volgorde.
                value = int("".join(digits))
                nums.append(value)

        problems.append((op_char, nums))

    return problems


def eval_problems(problems):
    """
    Bereken de grand total:
    - Per probleem: som of product van zijn getallen.
    - Daarna: som van alle probleem-uitkomsten.
    """
    grand_total = 0
    for op, nums in problems:
        if not nums:
            continue

        if op == "+":
            value = sum(nums)
        elif op == "*":
            value = 1
            for x in nums:
                value *= x
        else:
            raise ValueError(f"Onbekende operator: {op!r}")

        grand_total += value

    return grand_total


def solve(lines):
    problems = parse_worksheet(lines)
    return eval_problems(problems)


def run_test():
    test_lines = TEST_INPUT.splitlines()
    result = solve(test_lines)
    assert (
        result == EXPECTED_TEST_TOTAL
    ), f"Test faalt: verwacht {EXPECTED_TEST_TOTAL}, kreeg {result}"
    print(f"Test geslaagd, grand total = {result}")


def main():
    # 1. Test eerst met de voorbeeldinput (moet 3263827 zijn).
    run_test()

    # 2. Lees daarna de echte puzzelinput
    with open("input_puzzel_dag6.txt", encoding="utf-8") as f:
        lines = f.read().splitlines()

    total = solve(lines)
    print(f"Uitkomst voor input_puzzel_dag6.txt: {total}")


if __name__ == "__main__":
    main()