def compute_password_end_only(lines):
    """Oude methode: tel alleen keren dat de wijzer na een rotatie op 0 staat."""
    pos = 50
    count_zero = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        direction = line[0]
        distance = int(line[1:])

        if direction == 'R':
            pos = (pos + distance) % 100
        elif direction == 'L':
            pos = (pos - distance) % 100
        else:
            raise ValueError(f"Onbekende richting in regel: {line}")

        if pos == 0:
            count_zero += 1

    return count_zero


def zeros_during_rotation(pos, direction, distance):
    """
    Nieuwe methode-hulpje:
    tel hoeveel keer de wijzer tijdens deze éne rotatie op 0 komt,
    inclusief eventueel op het einde van de rotatie.
    """
    # Elke 100 klikken maak je een volledige ronde en kom je exact 1x langs 0.
    full_cycles = distance // 100
    rem = distance % 100

    zeros = full_cycles

    # Bepaal of we in de 'rest' van rem klikken nog een keer langs 0 komen.
    if direction == 'R':
        # Afstand tot de eerstvolgende 0 als je naar rechts draait.
        if pos == 0:
            dist_to_zero = 100  # je moet een hele ronde maken voordat je weer 0 raakt
        else:
            dist_to_zero = 100 - pos
    elif direction == 'L':
        # Afstand tot de eerstvolgende 0 als je naar links draait.
        if pos == 0:
            dist_to_zero = 100
        else:
            dist_to_zero = pos
    else:
        raise ValueError(f"Onbekende richting: {direction}")

    # Als we in de rem-klikken 0 nog halen, telt dat één extra keer.
    if rem >= dist_to_zero:
        zeros += 1

    return zeros


def compute_password_clicks(lines):
    """Nieuwe methode 0x434C49434B: tel elke klik waarop de wijzer op 0 staat."""
    pos = 50
    total_zeros = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        direction = line[0]
        distance = int(line[1:])

        # 1. Tel alle keren dat we tijdens deze rotatie op 0 terechtkomen.
        total_zeros += zeros_during_rotation(pos, direction, distance)

        # 2. Werk daarna de uiteindelijke positie bij.
        if direction == 'R':
            pos = (pos + distance) % 100
        elif direction == 'L':
            pos = (pos - distance) % 100
        else:
            raise ValueError(f"Onbekende richting in regel: {line}")

    return total_zeros


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
    assert compute_password_end_only(example_lines) == 3
    assert compute_password_clicks(example_lines) == 6
    print("Voorbeeldtest geslaagd: oud=3, nieuw=6")


def main():
    test_example()  # controleer met het voorbeeld uit de tekst

    with open("input_puzzel_dag1.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    old_password = compute_password_end_only(lines)
    new_password = compute_password_clicks(lines)

    print("Wachtwoord oude methode (einde van rotaties):", old_password)
    print("Wachtwoord nieuwe methode 0x434C49434B (alle klikken):", new_password)


if __name__ == "__main__":
    main()