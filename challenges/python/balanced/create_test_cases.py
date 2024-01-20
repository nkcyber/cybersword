# This was used during challenge development.
# You shouldn't need to use this again.

import json
from itertools import cycle, islice
from random import shuffle
from solution import is_balanced

sample_space = cycle("qp<>")

def get_length(n: int) -> list[str]:
    return list(islice(sample_space, n))

def get_randomized(n: int) -> str:
    l = get_length(n)
    shuffle(l)
    return ''.join(l)

def main():
    balanced = []
    not_balanced = []

    TARGET = 30
    while len(balanced) < TARGET or len(not_balanced) < TARGET:
        randomized = get_randomized(10)
        if is_balanced(randomized):
            if len(balanced) < TARGET:
                balanced.append(randomized)
        else:
            if len(not_balanced) < TARGET:
                not_balanced.append(randomized)


    test_cases = {}
    for bal in balanced:
        test_cases[bal] = True
    for bal in not_balanced:
        test_cases[bal] = False

    with open('test_cases.json', 'w') as f:
        json.dump(test_cases, f)

if __name__ == "__main__":
    main()
