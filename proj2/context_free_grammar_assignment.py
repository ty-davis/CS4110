from typing import List, Tuple

def is_regular_grammar(productions: List[Tuple[str, List[str]]]) -> bool:
    """
    Check if a grammar is regular.

    Args
    ----
    productions: List[Tuple[str, List[str]]]
        List of production rules in the grammar
        e.g. [('S', ['aA', 'A']), ('A', ['b', '^'])]

    Returns
    -------
    bool    True if grammar is regular, False otherwise
    """
    # terminals are lowercase, nonterminals are uppercase
    for lhs, rhss in productions:
        # ensure lhs is a single uppercase letter
        if not (lhs.isalpha() and len(lhs) == 1 and lhs.upper() == lhs):
            return False

        for rhs in rhss:
            # rhs must be at least 1 character long
            if len(rhs) < 1:
                return False
            elif len(rhs) == 1:
                # check for '^' first
                if rhs == '^':
                    continue

                # must be a terminal
                if not (rhs.isalpha() and rhs.lower() == rhs):
                    return False
            else: # 
                if not rhs.isalpha():
                    return False

                # non-terminal must be at the end, all others must be lower-case
                if not (rhs[:-1].lower() == rhs[:-1]):
                    return False

    return True


def recursive_parser(s: str) -> bool:
    """
    Recursive descent parser to check if string is balanced

    Args
    ----
    s: str
        Input string

    Returns
    -------
    bool: True if string is balanced, False otherwise
    """
    opening_brackets = ['[', '(', '{']
    closing_brackets = [']', ')', '}']

    # find first opening bracket
    min_open_idx = len(s) + 1
    first_bracket = ''
    for bracket in opening_brackets:
        idx = s.find(bracket)
        if idx >= 0 and idx < min_open_idx:
            min_open_idx = idx
            first_bracket = bracket

    if not first_bracket:
        # make sure there isn't a closing bracket if no opening brackets were found
        for bracket in closing_brackets:
            if bracket in s:
                return False
        else:
            return True

    # find its pair at the end
    close_idx = s.rfind(closing_brackets[opening_brackets.index(first_bracket)])
    if close_idx == -1:
        return False

    return recursive_parser(s[min_open_idx+1:close_idx]) and recursive_parser(s[close_idx+1:])


def stack_checker(s: str) -> bool:
    """
    stack-based balanced parentheses checker.

    Args
    ----
    s:  str
        Input string

    Returns
    -------
    bool:   True if string is balanced, False otherwise
    """
    opening_brackets = ['[', '(', '{']
    closing_brackets = [']', ')', '}']
    stack = []
    for c in s:
        if c in opening_brackets:
            stack.append(c)
            continue
        if c in closing_brackets:
            try:
                if opening_brackets.index(stack.pop()) != closing_brackets.index(c):
                    return False
            except IndexError:
                return False

    return len(stack) == 0

def test_balanced_parentheses():
    print("----- TESTING BALANCED PARENTHESES -----")
    test_cases = [
        ('()', True), ('[]', True), ('{}', True),
        ("([{}])", True), ("((()))", True), ("()[]", True),
        ("(]", False), ("([)]", False), ("((())", False),
        ("", True)
    ]

    for s, expected in test_cases:
        print(f"'{s}': ResursiveParser={recursive_parser(s)}, "
              f"StackChecker={stack_checker(s)}, Expected={expected}")

def test_regular_grammar():
    print("----- TESTING REGULAR GRAMMAR -----")
    # test cases with grammars including valid, invalid, empty production, invalid LHS, and mixed rules
    test_cases = [
        (
            [('S', ['aM', 'bS']), ('M', ['aF', 'bS']), ('F', ['aF', 'bF', '^'])],
            True
        ),
        (
            [('A', ['aB', 'c']), ('B', ['dB', '^'])],
            True
        ),
        (
            [('S1', ['aM']), ('M', ['b'])],
            False
        ),
        (
            [('S', ['aMb']), ('M', ['c'])],
            False
        ),
        (
            [('S', ['AB']), ('A', ['a']), ('B', ['b'])],
            False
        ),
        (
            [('S', ['aS', 'b']), ('A', ['Bb']), ('B', ['^'])],
            False
        ),
        (
            [('S', ['abS', 'cdM']), ('M', ['ef', '^'])],
            True
        ),
        (
            [('S', ['a', 'b', 'c', '^'])],
            True
        ),
    ]
    for case, expected in test_cases:
        print(f"'{case}'\n    Regular={is_regular_grammar(case)}, "
              f"Expected={expected}")


if __name__ == '__main__':
    test_balanced_parentheses()
    test_regular_grammar()
