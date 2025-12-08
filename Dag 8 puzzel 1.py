from __future__ import annotations

from typing import List, Tuple, Dict


# -----------------------------
# Hulpfuncties
# -----------------------------

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
    Disjoint Set Union / Union-Find datastructuur
    om efficiënt circuits (componenten) bij te houden.
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


def solve(points: List[Point], k_pairs: int) -> Tuple[int, List[int]]:
    """
    Verwerkt de k_pairs kortste paren (volgens Euclidische afstand in 3D),
    verbindt telkens de twee punten in hetzelfde circuit (component) via DSU,
    en retourneert:
      - het product van de drie grootste componentgroottes
      - de gesorteerde lijst van componentgroottes (aflopend)
    """
    n = len(points)
    dsu = DSU(n)

    # Alle paren en hun kwadratische afstand berekenen
    edges: List[Tuple[int, int, int]] = []  # (dist2, i, j)
    for i in range(n):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist2 = dx * dx + dy * dy + dz * dz
            edges.append((dist2, i, j))

    # Sorteer op afstand (kleinste eerst)
    edges.sort(key=lambda e: e[0])

    # Verwerk de eerste k_pairs kortste paren
    for idx in range(min(k_pairs, len(edges))):
        _, i, j = edges[idx]
        dsu.union(i, j)  # als ze al in zelfde circuit zitten, gebeurt "niets"

    # Componentgroottes verzamelen
    component_sizes: Dict[int, int] = {}
    for i in range(n):
        root = dsu.find(i)
        component_sizes[root] = component_sizes.get(root, 0) + 1

    sizes = sorted(component_sizes.values(), reverse=True)

    # Zorg dat we minstens 3 groottes hebben (zo niet, vul aan met 1)
    while len(sizes) < 3:
        sizes.append(1)

    product = sizes[0] * sizes[1] * sizes[2]
    return product, sizes


# -----------------------------
# Test op voorbeeldinput
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


def run_example_test() -> None:
    """
    Controleer dat de voorbeeldinput het gegeven antwoord 40 oplevert.
    """
    example_points = parse_points(EXAMPLE_TEXT)
    expected_product = 40  # uit de puzzelbeschrijving
    product, sizes = solve(example_points, k_pairs=10)
    assert product == expected_product, (
        f"Voorbeeld faalt: verwacht {expected_product}, kreeg {product}, "
        f"sizes={sizes}"
    )
    print("Voorbeeldtest OK. Product:", product, "Componentgroottes:", sizes)


# -----------------------------
# Main: eerst test, dan puzzel
# -----------------------------

def main() -> None:
    # 1) Test met voorbeeldinput (faalt -> programma stopt met AssertionError)
    run_example_test()

    # 2) Lees puzzelinput en los op met k_pairs=1000
    input_filename = "input_puzzel_dag8.txt"
    with open(input_filename, "r", encoding="utf-8") as f:
        puzzle_text = f.read()

    puzzle_points = parse_points(puzzle_text)
    product, sizes = solve(puzzle_points, k_pairs=1000)

    print("Puzzel: grootste drie componentgroottes:", sizes[:3])
    print("Antwoord (product van de drie grootste circuits):", product)


if __name__ == "__main__":
    main()