import heapq
import itertools
import re
from collections import namedtuple
from math import ceil

State = namedtuple("State", "ml cl mr cr boat")

LOADS = ((2, 0), (1, 1), (0, 2), (1, 0), (0, 1))
WEIGHT = {"M": 2, "C": 1}


def load_state(path="input.txt"):
    with open(path) as fh:
        raw = fh.read()
    digits = list(map(int, re.findall(r"\d+", raw)))[:4]
    side = re.findall(r"[LR]", raw.upper())[-1]
    return State(*digits, side)


def safe(ml, cl, mr, cr):
    if min(ml, cl, mr, cr) < 0:
        return False
    return not ((ml and cl > ml) or (mr and cr > mr))


def fare(m, c):
    return m * WEIGHT["M"] + c * WEIGHT["C"]


def moves_from(s):
    sign = -1 if s.boat == "L" else 1
    other = "R" if s.boat == "L" else "L"
    for m, c in LOADS:
        nxt = State(s.ml + sign * m, s.cl + sign * c,
                    s.mr - sign * m, s.cr - sign * c, other)
        if safe(*nxt[:4]):
            yield nxt, fare(m, c)


def weight_left(s):
    return s.ml * 2 + s.cl


def heur_weight(s):
    return weight_left(s)


def heur_packing(s):
    return ceil(weight_left(s) / 3)


def heur_returns(s):
    people = s.ml + s.cl
    if not people:
        return 0
    legs = ceil(people / 2)
    back = legs - 1 if s.boat == "L" else legs
    return weight_left(s) + back


HEURISTICS = {
    "Heuristic 1": heur_weight,
    "Heuristic 2": heur_packing,
    "Heuristic 3": heur_returns,
}


def search(start, h):
    tick = itertools.count()
    queue = [(h(start), next(tick), 0, start, (start,))]
    popped = 0
    while queue:
        _, _, g, cur, trail = heapq.heappop(queue)
        if cur.ml == 0 and cur.cl == 0:
            return trail, g, popped
        popped += 1
        for nxt, step in moves_from(cur):
            g2 = g + step
            heapq.heappush(queue, (g2 + h(nxt), next(tick), g2, nxt, trail + (nxt,)))
    return None, None, popped


def show(trail):
    return " -> ".join("({},{},{},{},{})".format(*s) for s in trail)


def main():
    start = load_state()
    for name, fn in HEURISTICS.items():
        trail, total, popped = search(start, fn)
        print(f"The solution of Q3.1 ({name}) is:")
        print("Solution Path:", show(trail) if trail else "No solution")
        print("Total cost =", total)
        print("Number of node expansions =", popped)
        print()


if __name__ == "__main__":
    main()