from collections import defaultdict
from functools import lru_cache
import sys


EXAMPLE_INPUT = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
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


def count_paths_with_constraints(graph, start="svr", target="out",
                                 must_visit=("dac", "fft")):
    """
    Tel alle paden van start naar target EN ook hoeveel daarvan alle
    knopen in `must_visit` (in willekeurige volgorde) bezoeken.

    We nemen aan dat de graaf geen oneindige lussen heeft.
    """

    # Voor deze puzzel zijn er precies twee verplichte knopen: dac en fft.
    # We coderen "bezocht" als een bitmask:
    # bit0 = dac bezocht?  bit1 = fft bezocht?
    node_to_bit = {}
    for i, node in enumerate(must_visit):
        node_to_bit[node] = 1 << i

    @lru_cache(maxsize=None)
    def dfs(node, visited_mask):
        """
        Geef een tuple terug:
        (totaal aantal paden vanaf deze state, aantal paden die eindigen
         in target én ALLE verplichte knopen hebben bezocht).
        """
        # Als we op dit node zijn, werk de visited_mask bij
        if node in node_to_bit:
            visited_mask |= node_to_bit[node]

        if node == target:
            # Eén pad gevonden. Dit pad voldoet alleen aan de voorwaarde
            # als alle bits van must_visit gezet zijn.
            all_bits = 0
            for b in node_to_bit.values():
                all_bits |= b
            meets_constraint = 1 if (visited_mask & all_bits) == all_bits else 0
            return 1, meets_constraint

        total_paths = 0
        constrained_paths = 0

        for nxt in graph.get(node, []):
            t, c = dfs(nxt, visited_mask)
            total_paths += t
            constrained_paths += c

        return total_paths, constrained_paths

    return dfs(start, 0)


def main():
    # 1) Controleer eerst met de voorbeeldinput uit de opgegeven tekst.
    example_graph = parse_graph(EXAMPLE_INPUT.splitlines())
    total_example, constrained_example = count_paths_with_constraints(
        example_graph, start="svr", target="out", must_visit=("dac", "fft")
    )

    # In de tekst staat: 8 paden totaal, waarvan 2 langs zowel dac als fft.
    if total_example != 8 or constrained_example != 2:
        print(
            f"FOUT in voorbeeldcheck:\n"
            f"  verwacht totaal=8, met_dac_en_fft=2\n"
            f"  maar kreeg totaal={total_example}, met_dac_en_fft={constrained_example}",
            file=sys.stderr,
        )
        sys.exit(1)

    # 2) Daarna de echte puzzelinput lezen.
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "input_puzzel_dag11.txt"

    with open(filename, encoding="utf-8") as f:
        puzzle_lines = f.readlines()

    puzzle_graph = parse_graph(puzzle_lines)
    total_paths, constrained_paths = count_paths_with_constraints(
        puzzle_graph, start="svr", target="out", must_visit=("dac", "fft")
    )

    print(f"Totaal aantal paden van 'svr' naar 'out': {total_paths}")
    print(
        f"Aantal paden van 'svr' naar 'out' die zowel 'dac' als 'fft' bezoeken: "
        f"{constrained_paths}"
    )


if __name__ == "__main__":
    main()