import re
from itertools import product

def parse_line(line):
    """
    Parse één regel:
    [.##.] (3) (1,3) ... { ... }
    -> target_bits (int), button_masks (list[int]), n_lights (int)
    """
    line = line.strip()
    if not line:
        return None

    # patroon tussen [ ]
    m_pat = re.search(r"\[(.*?)\]", line)
    pattern = m_pat.group(1)
    n_lights = len(pattern)

    target_bits = 0
    for i, ch in enumerate(pattern):
        if ch == "#":
            target_bits |= (1 << i)

    # alle knoppen (tussen haakjes)
    buttons = re.findall(r"\((.*?)\)", line)
    button_masks = []
    for b in buttons:
        b = b.strip()
        if not b:
            continue
        indices = [int(x) for x in b.split(",") if x.strip()]
        mask = 0
        for idx in indices:
            mask |= (1 << idx)
        button_masks.append(mask)

    return target_bits, button_masks, n_lights


def min_presses_for_machine(target_bits, button_masks, n_lights):
    """
    Zoek het minimale aantal drukken voor één machine.

    We modelleren A x = b over GF(2), waarbij:
    - x_i = 1 als knop i precies één keer wordt gedrukt (0 of 1 keer is genoeg).
    - A[j, i] = 1 als knop i lampje j toggelt.
    - b_j = doelstatus van lampje j (0 = uit, 1 = aan).

    Daarna zoeken we onder alle oplossingen x de oplossing met de kleinste Hamming-gewicht (aantal 1-en).
    """
    n_vars = len(button_masks)
    if n_vars == 0:
        # geen knoppen; kan alleen als target_bits == 0
        return 0 if target_bits == 0 else float("inf")

    # bouw rijen: per lampje een vergelijking
    # elke rij: (rowmask, rhs) waarbij rowmask bits over de knoppen zijn
    rows = []
    for light in range(n_lights):
        rowmask = 0
        for col, btn in enumerate(button_masks):
            if (btn >> light) & 1:
                rowmask |= (1 << col)
        rhs = (target_bits >> light) & 1
        rows.append([rowmask, rhs])

    # Gauss-eliminatie over GF(2) naar (bijna) RREF
    pivots = {}  # kolom -> rij
    row = 0
    m_rows = len(rows)

    for col in range(n_vars):
        # zoek pivot-rij met bit col = 1 vanaf 'row'
        pivot_row = None
        for r in range(row, m_rows):
            if (rows[r][0] >> col) & 1:
                pivot_row = r
                break
        if pivot_row is None:
            continue

        # zet pivot bovenaan
        rows[row], rows[pivot_row] = rows[pivot_row], rows[row]
        pivots[col] = row

        # elimineer deze kolom uit alle andere rijen (boven en onder)
        for r in range(m_rows):
            if r != row and ((rows[r][0] >> col) & 1):
                rows[r][0] ^= rows[row][0]
                rows[r][1] ^= rows[row][1]

        row += 1
        if row == m_rows:
            break

    # check inconsistentie: 0 = 1
    for rm, rhs in rows:
        if rm == 0 and rhs == 1:
            # geen oplossing; zou in deze puzzel niet moeten gebeuren
            return float("inf")

    # bepaal vrije en pivot-kolommen
    pivot_cols = sorted(pivots.keys())
    free_cols = [c for c in range(n_vars) if c not in pivots]

    # 1) specifieke oplossing x0 (alle vrije variabelen = 0)
    x0 = 0
    for pcol in pivot_cols:
        r = pivots[pcol]
        val = rows[r][1]  # rhs in RREF
        if val & 1:
            x0 |= (1 << pcol)

    # 2) basis voor de nulruimte (homogene oplossingen A x = 0)
    # voor elke vrije kolom fc construeren we een basisvector v
    basis = []
    for fc in free_cols:
        v = 0
        # vrije variabele zelf = 1
        v |= (1 << fc)
        # elke pivot-variabele is xor van vrije variabelen in zijn rij
        for pcol in pivot_cols:
            r = pivots[pcol]
            if (rows[r][0] >> fc) & 1:
                # coefficient is 1 -> pivot hangt af van deze vrije var
                v ^= (1 << pcol)
        basis.append(v)

    # 3) doorloop alle combinaties van basisvectors en zoek min popcount
    d = len(basis)
    # als er geen vrije variabelen zijn, is x0 de enige oplossing
    if d == 0:
        return x0.bit_count()

    best = float("inf")
    # brute-force over 2^d combinaties; in dergelijke puzzels is d normaal klein
    for mask in range(1 << d):
        x = x0
        bit = 0
        m = mask
        while m:
            if m & 1:
                x ^= basis[bit]
            m >>= 1
            bit += 1
        w = x.bit_count()
        if w < best:
            best = w

    return best


def solve_text(text):
    """
    Neemt de volledige input als string en geeft
    het totaal minimaal aantal drukken over alle machines.
    """
    total = 0
    for line in text.splitlines():
        parsed = parse_line(line)
        if not parsed:
            continue
        target_bits, button_masks, n_lights = parsed
        total += min_presses_for_machine(target_bits, button_masks, n_lights)
    return total


def main():
    # 1) check met de gegeven testinput
    test_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
    test_result = solve_text(test_input)
    print("Testresultaat:", test_result)
    assert test_result == 7, f"Verwacht 7, kreeg {test_result}"
    print("Test OK")

    # 2) nu de echte puzzelinput
    with open("input_puzzel_dag10.txt", encoding="utf-8") as f:
        puzzle_input = f.read()
    answer = solve_text(puzzle_input)
    print("Antwoord voor input_puzzel_dag10.txt:", answer)


if __name__ == "__main__":
    main()