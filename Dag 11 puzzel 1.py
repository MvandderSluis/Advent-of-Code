from collections import defaultdict
from functools import lru_cache
import sys


EXAMPLE_INPUT = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""


def parse_graph(lines):
    """
    Parse regels van de vorm:
    naam: doel1 doel2 ...
    naar een adjacency list (dict: device -> list van volgende devices).
    """
    graph = defaultdict(list)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        left, right = line.split(":")
        src = left.strip()
        dests = right.strip().split()
        graph[src] = dests
    return graph


def count_paths(graph, start="you", target="out"):
    """
    Tel het aantal verschillende paden van start naar target in een gerichte graaf.

    We nemen aan dat er geen oneindige lussen zijn (oftewel effectief een DAG),
    zoals gebruikelijk in dit soort puzzels.
    """

    @lru_cache(maxsize=None)
    def dfs(node):
        # Bereik je het eind-device, dan heb je precies 1 pad gevonden.
        if node == target:
            return 1

        total = 0
        for nxt in graph.get(node, []):
            total += dfs(nxt)
        return total

    return dfs(start)


def main():
    # 1) Eerst controleren met de testinput uit de puzzeltekst.
    example_graph = parse_graph(EXAMPLE_INPUT.splitlines())
    example_result = count_paths(example_graph, "you", "out")

    if example_result != 5:
        # Als dit gebeurt, klopt de implementatie niet en stoppen we.
        print(
            f"FOUT: verwacht 5 paden voor de voorbeeldinput, "
            f"maar kreeg {example_result}.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 2) Daarna de echte puzzelinput lezen.
    # Standaard uit 'input_puzzel_dag11.txt', maar je kunt ook een bestandsnaam
    # meegeven als eerste command-line argument.
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "input_puzzel_dag11.txt"

    with open(filename, encoding="utf-8") as f:
        puzzle_lines = f.readlines()

    puzzle_graph = parse_graph(puzzle_lines)
    result = count_paths(puzzle_graph, "you", "out")

    print(f"Aantal verschillende paden van 'you' naar 'out': {result}")


if __name__ == "__main__":
    main()