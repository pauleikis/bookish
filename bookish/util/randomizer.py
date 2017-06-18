from random import random
from bisect import bisect
from typing import List

from bookish.model import Translation


def pick_one(items: List[Translation]) -> Translation:
    weights = list(map(weight, items))
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random() * total
    i = bisect(cum_weights, x)
    return items[i]


def weight(item: Translation) -> float:
    attempts = item.attempts
    successes = item.successes
    tier = item.tier
    return ((attempts - successes) / attempts) ** tier
