from __future__ import annotations

from typing import List, Tuple, Dict


Point = Tuple[int, int, int]


def parse_points(text: str) -> List[Point]:
    """
    Parseert regels van de vorm 'X,Y,Z' naar een lijst van (x, y, z)-tuples.
    Lege regels worden genegeerd.
    """
    points: List[Point] = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        x_str, y_str, z_str = line.split(",")
        points.append((int(x_str), int(y_str), int(z_str)))
    return points


class DSU:
    """
    Disjoint Set Union / Union-Find om circuits (componenten) bij te houden.
    """

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, a: int) -> int:
        # Path compression
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a: int, b: int) -> bool:
        """
        Voegt de componenten van a en b samen (indien verschillend).
        Retourneert True als er echt samengevoegd is, False als ze al samen waren.
        """
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        # Union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def build_sorted_edges(points: List[Point]) -> List[Tuple[int, int, int]]:
    """
    Maak alle paren (i, j) met hun kwadratische afstand en sorteer op afstand.
    Retourneert lijst van tuples: (dist2, i, j).
    """
    n = len(points)
    edges: List[Tuple[int, int, int]] = []
    for i in range(n):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist2 = dx * dx + dy * dy + dz * dz
            edges.append((dist2, i, j))
    edges.sort(key=lambda e: e[0])
    return edges


# -----------------------------
# Deel 1: eerste k kortste verbindingen
# -----------------------------

def solve_part1(points: List[Point], k_pairs: int) -> Tuple[int, List[int]]:
    """
    Verwerkt de k_pairs kortste paren, houdt circuits bij met DSU
    en geeft:
      - het product van de drie grootste circuits,
      - de volledige lijst componentgroottes (aflopend gesorteerd).
    """
    n = len(points)
    dsu = DSU(n)
    edges = build_sorted_edges(points)

    for idx in range(min(k_pairs, len(edges))):
        _, i, j = edges[idx]
        dsu.union(i, j)

    # Componentgroottes bepalen
    component_sizes: Dict[int, int] = {}
    for i in range(n):
        root = dsu.find(i)
        component_sizes[root] = component_sizes.get(root, 0) + 1

    sizes = sorted(component_sizes.values(), reverse=True)

    while len(sizes) < 3:
        sizes.append(1)

    product = sizes[0] * sizes[1] * sizes[2]
    return product, sizes


# -----------------------------
# Deel 2: doorgaan tot één circuit
# -----------------------------

def solve_part2(points: List[Point]) -> Tuple[int, Tuple[int, int], int, int]:
    """
    Verbindt steeds de volgende kortste paren totdat alle punten
    in één circuit zitten.

    Retourneert:
      - product_x: product van de X-coördinaten van de laatste twee
                   junction boxes die samengevoegd worden.
      - last_pair: (i, j) indices van die twee punten
      - last_dist2: kwadratische afstand van die laatste verbinding
      - steps: aantal verwerkte paren tot en met deze laatste verbinding
    """
    n = len(points)
    dsu = DSU(n)
    edges = build_sorted_edges(points)

    components = n
    last_pair: Tuple[int, int] | None = None
    last_dist2: int | None = None
    steps = 0

    for dist2, i, j in edges:
        merged = dsu.union(i, j)
        steps += 1
        if merged:
            components -= 1
            if components == 1:
                last_pair = (i, j)
                last_dist2 = dist2
                break

    if last_pair is None or last_dist2 is None:
        raise RuntimeError("Het is niet gelukt om alle punten in één circuit te krijgen.")

    i, j = last_pair
    x1 = points[i][0]
    x2 = points[j][0]
    product_x = x1 * x2
    return product_x, last_pair, last_dist2, steps


# -----------------------------
# Voorbeeldinput + tests
# -----------------------------

EXAMPLE_TEXT = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


def run_example_tests() -> None:
    example_points = parse_points(EXAMPLE_TEXT)

    # Deel 1: na 10 verbindingen product drie grootste circuits = 40
    expected_part1 = 40
    product1, sizes = solve_part1(example_points, k_pairs=10)
    assert product1 == expected_part1, (
        f"Voorbeeld deel 1 faalt: verwacht {expected_part1}, "
        f"kreeg {product1}, sizes={sizes}"
    )

    # Deel 2: laatste verbinding: X=216 en X=117 => 25272
    expected_part2 = 25272
    product2, last_pair, _, steps = solve_part2(example_points)
    assert product2 == expected_part2, (
        f"Voorbeeld deel 2 faalt: verwacht {expected_part2}, "
        f"kreeg {product2}, last_pair={last_pair}, steps={steps}"
    )

    print("Voorbeeldtest deel 1 OK. Product:", product1, "Componentgroottes:", sizes)
    print(
        "Voorbeeldtest deel 2 OK. Product X-coördinaten laatste verbinding:",
        product2,
        "Laatste pair indices:",
        last_pair,
        "Na aantal verwerkte paren:",
        steps,
    )


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    # 1) Test met voorbeeldinput
    run_example_tests()

    # 2) Lees puzzelinput
    input_filename = "input_puzzel_dag8.txt"
    with open(input_filename, "r", encoding="utf-8") as f:
        puzzle_text = f.read()

    puzzle_points = parse_points(puzzle_text)

    # Deel 1: eerste 1000 kortste verbindingen
    product1, sizes = solve_part1(puzzle_points, k_pairs=1000)
    print("Puzzel deel 1:")
    print("  Grootste drie componentgroottes:", sizes[:3])
    print("  Antwoord (product van de drie grootste circuits):", product1)

    # Deel 2: doorgaan tot één circuit
    product2, last_pair, last_dist2, steps = solve_part2(puzzle_points)
    i, j = last_pair
    x1, x2 = puzzle_points[i][0], puzzle_points[j][0]
    print("\nPuzzel deel 2:")
    print("  Laatste verbinding tussen indices:", last_pair)
    print("  Coördinaten punt 1:", puzzle_points[i])
    print("  Coördinaten punt 2:", puzzle_points[j])
    print("  Kwadratische afstand laatste verbinding:", last_dist2)
    print("  Verwerkte paren tot deze verbinding:", steps)
    print("  Antwoord (product van X-coördinaten):", product2)


if __name__ == "__main__":
    main()