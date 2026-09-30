import heapq
import itertools
import re
from collections import namedtuple
from math import ceil

State = namedtuple("State", "ml cl mr cr boat")

LOADS = ((2, 0), (1, 1), (0, 2), (1, 0), (0, 1))
WEIGHT = {"M": 2, "C": 1}