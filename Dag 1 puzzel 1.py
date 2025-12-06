def compute_password(lines):
    pos = 50        # startpositie
    count_zero = 0  # aantal keren dat de wijzer op 0 staat na een rotatie

    for line in lines:
        line = line.strip()
        if not line:
            continue  # sla lege regels over

        direction = line[0]          # 'L' of 'R'
        distance = int(line[1:])     # rest is het getal

        if direction == 'R':
            pos = (pos + distance) % 100
        elif direction == 'L':
            pos = (pos - distance) % 100
        else:
            raise ValueError(f"Onbekende richting in regel: {line}")

        if pos == 0:
            count_zero += 1

    return count_zero


def test_example():
    example_lines = [
        "L68",
        "L30",
        "R48",
        "L5",
        "R60",
        "L55",
        "L1",
        "L99",
        "R14",
        "L82",
    ]
    assert compute_password(example_lines) == 3
    print("Voorbeeldtest geslaagd: wachtwoord = 3")


def main():
    test_example()  # controleer eerst het voorbeeld

    with open("input_puzzel_dag1.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    password = compute_password(lines)
    print("Het wachtwoord is:", password)


if __name__ == "__main__":
    main()