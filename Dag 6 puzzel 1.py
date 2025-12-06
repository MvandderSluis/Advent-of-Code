# dag6_cephalopod_math.py

TEST_INPUT = """123 328  51  64
 45  64 387  23
  6  98 215 314
  *   +   *   +"""

EXPECTED_TEST_TOTAL = 4277556


def parse_worksheet(lines):
    """
    Zet de ruwe tekstregels om in een lijst van problemen.
    Elk probleem is een tuple: (operator, [getallen]).
    """
    # Zorg dat alle regels even lang zijn en behoud spaties.
    width = max(len(line) for line in lines)
    grid = [line.rstrip("\n").ljust(width) for line in lines]

    nrows = len(grid)
    ncols = width

    # Bepaal per kolom of er ergens een niet-spatie staat (dan hoort hij bij een probleem).
    content_cols = []
    for c in range(ncols):
        has_content = any(grid[r][c] != " " for r in range(nrows))
        content_cols.append(has_content)

    # Groepeer opeenvolgende content-kolommen tot segmenten (één segment = één probleem).
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
        # Onderste regel van dit segment: hier staat precies één operator (+ of *).
        bottom_slice = grid[-1][start : end + 1]
        op_char = None

        for ch in bottom_slice:
            if ch in "+*":
                if op_char is not None:
                    raise ValueError("Meer dan één operator in een probleemsegment.")
                op_char = ch

        if op_char is None:
            # Geen operator = geen geldig probleem; eventueel overslaan of fout gooien.
            continue

        # Boven de onderste regel staan de getallen, elk in zijn eigen rij (mogelijk met spaties).
        nums = []
        for r in range(nrows - 1):
            snippet = grid[r][start : end + 1]
            s = snippet.strip()
            if s:
                # Normaliter alleen cijfers; mocht er wat anders doorheen glippen, filter.
                if not s.isdigit():
                    s = "".join(ch for ch in s if ch.isdigit())
                if s:
                    nums.append(int(s))

        problems.append((op_char, nums))

    return problems


def eval_problems(problems):
    """
    Bereken de grand total: voor elk probleem eerst de som of het product
    van zijn getallen, daarna alle uitkomsten bij elkaar optellen.
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
    # 1. Test eerst met de voorbeeldinput
    run_test()

    # 2. Lees daarna de echte puzzelinput
    with open("input_puzzel_dag6.txt", encoding="utf-8") as f:
        lines = f.read().splitlines()

    total = solve(lines)
    print(f"Uitkomst voor input_puzzel_dag6.txt: {total}")


if __name__ == "__main__":
    main()