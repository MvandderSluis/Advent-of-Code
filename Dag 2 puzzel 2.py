import sys
import os
from typing import List, Tuple


def parse_ranges(line: str) -> List[Tuple[int, int]]:
    """
    Parse a single line like:
        11-22,95-115,998-1012,...
    into a list [(11, 22), (95, 115), ...].
    """
    parts = [p.strip() for p in line.split(",") if p.strip()]
    ranges = []
    for part in parts:
        start_str, end_str = part.split("-")
        ranges.append((int(start_str), int(end_str)))
    return ranges


def find_invalid_ids_in_range(L: int, R: int):
    """
    Nieuwe regels:
    Een ID is ongeldig als de decimale representatie bestaat uit
    een blok digits dat minstens twee keer herhaald wordt:

        s = t t ... t   (k >= 2)

    waarbij t geen leidende nul heeft.
    """
    invalids = set()

    len_L = len(str(L))
    len_R = len(str(R))

    # total_len is het aantal digits van het getal
    for total_len in range(len_L, len_R + 1):
        # m = lengte van het blok t
        # We eisen: m is een deler van total_len en total_len / m >= 2
        for m in range(1, total_len // 2 + 1):
            if total_len % m != 0:
                continue

            k = total_len // m  # aantal herhalingen
            if k < 2:
                continue

            pow_m = 10 ** m

            # rep_factor = 111...1 in "base 10^m" (k keer '1').
            # Bijvoorbeeld m=2, k=3 -> factor = 10^4 + 10^2 + 1 = 10101
            rep_factor = 0
            for _ in range(k):
                rep_factor = rep_factor * pow_m + 1

            # t heeft precies m digits (geen leidende nul)
            t_min = 10 ** (m - 1)
            t_max = pow_m - 1

            # We willen L <= t * rep_factor <= R
            # => grenzen voor t
            t_lower_bound = (L + rep_factor - 1) // rep_factor  # ceil(L / rep_factor)
            t_upper_bound = R // rep_factor                      # floor(R / rep_factor)

            t_start = max(t_min, t_lower_bound)
            t_end = min(t_max, t_upper_bound)

            if t_start > t_end:
                continue

            for t in range(t_start, t_end + 1):
                x = t * rep_factor
                if L <= x <= R:
                    invalids.add(x)

    return sorted(invalids)


def sum_invalid_ids_in_range(L: int, R: int) -> int:
    return sum(find_invalid_ids_in_range(L, R))


def run_example_test():
    example = (
        "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
        "1698522-1698528,446443-446449,38593856-38593862,"
        "565653-565659,824824821-824824827,2121212118-2121212124"
    )

    ranges = parse_ranges(example)

    print("=== Example Test (nieuwe regels) ===")
    grand_total = 0

    for (L, R) in ranges:
        invalids = find_invalid_ids_in_range(L, R)
        print(f"Range {L}-{R}: invalid IDs → {invalids}")
        grand_total += sum(invalids)

    print("\nTotal sum of invalid IDs (example):")
    print(grand_total)
    print("Expected: 4174379265\n")


def main():
    # 1. Eerst de voorbeelddata controleren
    run_example_test()

    # 2. Daarna je echte input uit het bestand
    filename = "input_puzzel_dag2.txt"

    if not os.path.exists(filename):
        print(f"Error: Could not find file '{filename}'.", file=sys.stderr)
        return

    with open(filename, "r") as f:
        data = f.read().strip()

    if not data:
        print("Error: File was empty.")
        return

    ranges = parse_ranges(data)
    answer = sum(sum_invalid_ids_in_range(L, R) for (L, R) in ranges)

    print("=== Puzzle Result (nieuwe regels) ===")
    print("Sum of all invalid IDs:")
    print(answer)


if __name__ == "__main__":
    main()