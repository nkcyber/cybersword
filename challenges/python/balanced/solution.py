# this is a custom problem built to test a student's understanding of stack memory
# it's very similar to https://leetcode.com/problems/valid-parentheses

"""
Reversing '<' makes '>'.
Reversing 'q' makes 'p'.

is_balanced is a funciton that takes a string of the characters '<>qp', and returns whether the string is balanced.

Every opening '<' must be matched with a closing '>'.
Every opening 'q' must be matched with a closing 'p'.

Examples:
    - is_balanced("") -> True
    - is_balanced("<>") -> True
    - is_balanced("qp") -> True
    - is_balanced("q<>p") -> True
    - is_balanced("<qpqp>qp") -> True
    - is_balanced("<qp") -> False
    - is_balanced("><") -> False
    - is_balanced("q>") -> False

def is_balanced(chars: str) -> bool:
    ...
"""

def is_balanced(letters: str) -> bool:
    stack = []
    for letter in letters:
        if letter in '<q': # starting 1 or 2
            stack.append(letter)
        elif letter == '>': # ending 1
            if len(stack) > 0 and stack.pop() != '<':
                return False
        elif letter == 'p': # ending 2
            if len(stack) > 0 and stack.pop() != 'q':
                return False
    return len(stack) == 0


if __name__ == "__main__":
    for letters in ("", "<>", "qp", "q<>p", "<qpqp>qp", "<qp", "><", "q>"):
        print(f'is_balanced("{letters}") -> {is_balanced(letters)}')

