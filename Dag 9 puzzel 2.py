from typing import List, Tuple


def parse_points(text: str) -> List[Tuple[int, int]]:
    points = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        x_str, y_str = line.split(",")
        points.append((int(x_str), int(y_str)))
    return points


def build_edges(points: List[Tuple[int, int]]):
    """Maak lijst van polygon-randen uit de rode punten (gesloten lus)."""
    n = len(points)
    edges = []
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        edges.append(((x1, y1), (x2, y2)))
    return edges


def point_on_segment(px: float, py: float, x1: int, y1: int, x2: int, y2: int) -> bool:
    """Check of punt (px,py) op het (axis-aligned) segment ligt."""
    if x1 == x2:  # verticaal
        if px != x1:
            return False
        return min(y1, y2) <= py <= max(y1, y2)
    if y1 == y2:  # horizontaal
        if py != y1:
            return False
        return min(x1, x2) <= px <= max(x1, x2)
    return False  # in deze puzzel zijn alle segmenten axis-aligned


def make_point_in_or_on_polygon(points: List[Tuple[int, int]]):
    """Maak een point-in-polygon functie (axis-aligned, gesloten polygon)."""
    edges = build_edges(points)

    def point_in_or_on_polygon(pt: Tuple[float, float]) -> bool:
        x, y = pt
        # 1. Eerst: ligt het punt op de rand?
        for (x1, y1), (x2, y2) in edges:
            if point_on_segment(x, y, x1, y1, x2, y2):
                return True

        # 2. Ray casting naar rechts, alleen verticale randen tellen
        cnt = 0
        for (x1, y1), (x2, y2) in edges:
            if x1 != x2:  # horizontale rand
                continue
            vx = x1
            ymin, ymax = sorted((y1, y2))
            # snijvoorwaarde: y in [ymin, ymax) en rand rechts van punt
            if ymin <= y < ymax and vx > x:
                cnt += 1

        return (cnt % 2) == 1

    return point_in_or_on_polygon, edges


def largest_rectangle_red_green(points: List[Tuple[int, int]]) -> int:
    """
    Zoek de grootste rechthoek met:
    - twee rode tegels als tegenoverliggende hoeken
    - ALLE tegels binnen de rechthoek liggen binnen of op de rode/groene lus.
    """
    if len(points) < 2:
        return 0

    point_in_or_on_polygon, edges = make_point_in_or_on_polygon(points)
    n = len(points)

    def rectangle_inside_polygon(x1: int, y1: int, x2: int, y2: int) -> bool:
        # Degeneraat 1x1: één tegel, en die is rood -> altijd oké.
        if x1 == x2 and y1 == y2:
            return True

        X1, X2 = sorted((x1, x2))
        Y1, Y2 = sorted((y1, y2))

        # Middelpunt van de rechthoek in continue ruimte
        cx = (X1 + X2) / 2.0
        cy = (Y1 + Y2) / 2.0

        # Als het middelpunt niet binnen de polygon ligt, kan de hele rechthoek
        # nooit volledig binnen de lus liggen.
        if not point_in_or_on_polygon((cx, cy)):
            return False

        open_has_x = X1 < X2
        open_has_y = Y1 < Y2

        # Dikke rechthoek: er is een echte "interior" (open gebied)
        if open_has_x and open_has_y:
            # Check of een polygonrand door het open inwendige van de rechthoek loopt.
            # Als dat zo is, moet een deel van de rechthoek buiten liggen.
            for (ax, ay), (bx, by) in edges:
                if ax == bx:  # verticale rand
                    vx = ax
                    sy, ey = sorted((ay, by))
                    if X1 < vx < X2:
                        if max(sy, Y1) < min(ey, Y2):
                            return False
                else:  # horizontale rand
                    vy = ay
                    sx, ex = sorted((ax, bx))
                    if Y1 < vy < Y2:
                        if max(sx, X1) < min(ex, X2):
                            return False
        else:
            # Dunne rechthoek (breedte 1 of hoogte 1):
            # we doen een strengere check op de eindpunten.
            if not point_in_or_on_polygon((x1, y1)):
                return False
            if not point_in_or_on_polygon((x2, y2)):
                return False

        return True

    max_area = 0

    # Alle paren rode tegels als tegenoverliggende hoeken
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if area <= max_area:
                continue
            if rectangle_inside_polygon(x1, y1, x2, y2):
                max_area = area

    return max_area


def main():
    # 1. Test met de voorbeeldinput (verwacht 24)
    test_input = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
    test_points = parse_points(test_input)
    test_result = largest_rectangle_red_green(test_points)
    print("Testresultaat (voorbeeld):", test_result)
    assert test_result == 24, f"Test faalt: verwacht 24, kreeg {test_result}"

    # 2. Daarna de echte puzzelinput gebruiken
    with open("input_puzzel_dag9.txt", "r", encoding="utf-8") as f:
        puzzle_text = f.read()

    puzzle_points = parse_points(puzzle_text)
    puzzle_result = largest_rectangle_red_green(puzzle_points)
    print("Antwoord voor input_puzzel_dag9.txt:", puzzle_result)


if __name__ == "__main__":
    main()