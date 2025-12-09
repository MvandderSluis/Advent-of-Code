def parse_points(text: str):
    points = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        x_str, y_str = line.split(",")
        points.append((int(x_str), int(y_str)))
    return points


def largest_rectangle(points):
    """
    points: lijst met (x, y)-paren, met 0,0 linksboven.
    Een rechthoek wordt bepaald door twee tegenoverliggende rode hoeken.
    De randen lopen door de twee hoeken heen (inclusief).
    """
    n = len(points)
    if n < 2:
        return 0

    max_area = 0
    # bekijk alle paren rode tegels
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            # breedte/hoogte zijn inclusief beide hoeken
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            if area > max_area:
                max_area = area
    return max_area


def main():
    # --- 1. Test met de voorbeeldinput uit de opgave ---
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
    test_result = largest_rectangle(test_points)
    print("Testresultaat (voorbeeld):", test_result)
    assert test_result == 50, "Test faalt: verwacht 50, kreeg {}".format(test_result)

    # --- 2. Daarna de echte puzzelinput gebruiken ---
    # Verwacht bestand: input_puzzel_dag9.txt in dezelfde map
    with open("input_puzzel_dag9.txt", "r", encoding="utf-8") as f:
        puzzle_text = f.read()

    puzzle_points = parse_points(puzzle_text)
    puzzle_result = largest_rectangle(puzzle_points)
    print("Antwoord voor input_puzzel_dag9.txt:", puzzle_result)


if __name__ == "__main__":
    main()