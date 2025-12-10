import re
from pathlib import Path
import pulp


def parse_line(line):
    buttons = [
        list(map(int, part.split(",")))
        for part in re.findall(r"\(([^)]*)\)", line)
        if part.strip()
    ]
    target = list(
        map(int, re.search(r"\{([^}]*)\}", line).group(1).split(","))
    )
    return buttons, target


def min_presses_ilp(buttons, target):
    prob = pulp.LpProblem("Joltage", pulp.LpMinimize)

    # Variabelen: hoeveel keer elke knop wordt ingedrukt
    x = [
        pulp.LpVariable(f"x_{j}", lowBound=0, cat="Integer")
        for j in range(len(buttons))
    ]

    # Doelfunctie
    prob += pulp.lpSum(x)

    # Constraints per counter
    for i in range(len(target)):
        prob += (
            pulp.lpSum(x[j] for j, b in enumerate(buttons) if i in b)
            == target[i]
        )

    # Oplossen
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if prob.status != pulp.LpStatusOptimal:
        raise RuntimeError("Geen optimale oplossing gevonden")

    return sum(int(v.value()) for v in x)


def solve_text(text):
    total = 0
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        buttons, target = parse_line(line)
        total += min_presses_ilp(buttons, target)
    return total


def main():
    # ======================
    # TESTINPUT
    # ======================
    test_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
    result = solve_text(test_input)
    print("Testresultaat:", result)
    assert result == 33, "Testinput faalt"
    print("✅ Testinput correct")

    # ======================
    # ECHTE INPUT
    # ======================
    p = Path("input_puzzel_dag10.txt")
    print("Antwoord:", solve_text(p.read_text()))


if __name__ == "__main__":
    main()