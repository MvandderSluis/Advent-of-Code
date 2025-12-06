import sys
from typing import List, Tuple
import os

def parse_ranges(line: str) -> List[Tuple[int, int]]:
    parts = [p.strip() for p in line.split(",") if p.strip()]
    ranges = []
    for part in parts:
        start_str, end_str = part.split("-")
        ranges.append((int(start_str), int(end_str)))
    return ranges


def find_invalid_ids_in_range(L: int, R: int) -> List[int]:
    """
    Return all invalid IDs in [L, R].
    Invalid ID = a decimal string of even length with first half == second half.
    """
    invalids = []

    len_L = len(str(L))
    len_R = len(str(R))

    for full_len in range(len_L, len_R + 1):
        if full_len % 2 != 0:
            continue

        half_len = full_len // 2
        base = 10 ** half_len
        factor = base + 1

        t_min = 10 ** (half_len - 1)
        t_max = base - 1

        t_lower_bound = (L + factor - 1) // factor
        t_upper_bound = R // factor

        t_start = max(t_min, t_lower_bound)
        t_end = min(t_max, t_upper_bound)

        if t_start > t_end:
            continue

        for t in range(t_start, t_end + 1):
            x = t * factor
            if L <= x <= R:
                invalids.append(x)

    return invalids


def sum_invalid_ids_in_range(L: int, R: int) -> int:
    return sum(find_invalid_ids_in_range(L, R))


def run_example_test():
    example = (
        "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
        "1698522-1698528,446443-446449,38593856-38593862,"
        "565653-565659,824824821-824824827,2121212118-2121212124"
    )

    ranges = parse_ranges(example)

    print("=== Example Test ===")
    grand_total = 0

    for (L, R) in ranges:
        invalids = find_invalid_ids_in_range(L, R)
        if invalids:
            print(f"Range {L}-{R}: invalid IDs → {invalids}")
        else:
            print(f"Range {L}-{R}: (none)")
        grand_total += sum(invalids)

    print("\nTotal sum of invalid IDs:")
    print(grand_total)
    print("(Expected: 4174379265)\n")


def main():
    # Run built-in example test
    run_example_test()

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

    print("=== Puzzle Result ===")
    print("Sum of all invalid IDs:")
    print(answer)


if __name__ == "__main__":
    main()