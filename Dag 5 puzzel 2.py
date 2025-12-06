def parse_ranges(ranges_str: str):
    """Parse lines 'start-end' into a list of (start, end) integer tuples."""
    ranges = []
    for line in ranges_str.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        start_str, end_str = line.split("-")
        ranges.append((int(start_str), int(end_str)))
    return ranges


def merge_ranges(ranges):
    """Merge overlapping or touching ranges."""
    if not ranges:
        return []

    # Sort ranges by starting point
    ranges.sort()
    merged = [ranges[0]]

    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]

        if start <= last_end + 1:
            # Overlap or touching: merge
            merged[-1] = (last_start, max(last_end, end))
        else:
            # No overlap
            merged.append((start, end))

    return merged


def count_total_ids(ranges):
    """Count how many unique IDs are represented by merged ranges."""
    total = 0
    for start, end in ranges:
        total += (end - start + 1)
    return total


def main():
    filename = "input_puzzel_dag5.txt"
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Use only the first section (ranges)
    parts = content.split("\n\n", 1)
    ranges_part = parts[0]

    ranges = parse_ranges(ranges_part)
    merged = merge_ranges(ranges)
    total_ids = count_total_ids(merged)

    print("Totaal aantal ingredient IDs dat vers is volgens de ranges:", total_ids)


if __name__ == "__main__":
    main()