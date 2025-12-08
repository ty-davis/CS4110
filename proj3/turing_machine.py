from typing import List, Dict

class Rule:
    def __init__(self, state: int, read_symbol: str, write_symbol: str, next_state: int, direction: str):
        """
        Initialize a Turing Machine rule.

        Parameters
        ----------
        state           Current state of the Turing Machine
        read_symbol     Symbol to read from the tape
        write_symbol    Symbol to write to the tape
        next_state      State to transition to
        direction       Direction to move the head ('L' or 'R')
        """
        self.state: int = state
        self.next_state: int = next_state

        if len(read_symbol) != 1:
            raise ValueError("read_symbol must be one character long")
        self.read_symbol: str = read_symbol
        if len(write_symbol) != 1:
            raise ValueError("write_symbol must be one character long")
        self.write_symbol:str = write_symbol


        if direction not in ('L', 'R'):
            raise ValueError("direction must be 'L' or 'R'")
        self.direction: str = direction

    @property
    def hash(self):
        """
        Get the hash of this rule.

        Returns
        -------
        str Hash of the rule based on state and read_symbol
        """
        return Rule.make_hash(self.state, self.read_symbol)

    @staticmethod
    def make_hash(state, read_symbol) -> str:
        """
        Create a hash key for rule lookup.

        Parameters
        ----------
        state           State of the rule
        read_symbol     Symbol to read from the tape

        Returns
        -------
        str Hash key for rule lookup
        """
        return f"{state}{read_symbol}"

class TuringMachine:
    def __init__(self, rules: List[Rule], input_symbols: str, tape_symbols: str, blank_symbol: str, start_state: int, halt_states: List[int]):
        """
        Creates a Turing Machine from a list of rules structured like the
        table in the lectures.
        """
        self.head: int = 0
        self.tape: str | None = None
        self.current_state: int = start_state
        self.input_symbols: str = input_symbols
        self.tape_symbols: str = tape_symbols
        self.blank_symbol: str = blank_symbol
        self.halt_states: List[int] = halt_states
        self.rules: Dict[str, Rule] = {rule.hash: rule for rule in rules}

    def set_input(self, input_string):
        """
        Load an input string onto the tape.

        Parameters
        ----------
        input_string    Input string to load onto the tape
        """
        for symbol in input_string:
            if symbol not in self.input_symbols:
                raise ValueError("Invalid input symbol")
        self.tape = input_string

    def read_tape(self):
        """
        Read the symbol at the current head position.

        Returns
        -------
        str Symbol at the current head position
        """
        n = self.head
        if n < 0:
            raise ValueError("Cannot read from left of first cell")
        if not self.tape:
            raise ValueError("Input not yet provided to Turing Machine")
        if n > len(self.tape) - 1:
            return self.blank_symbol
        return self.tape[n]

    def write_tape(self, char: str):
        """
        Write a character at the current head position.

        Parameters
        ----------
        char    Character to write at the current head position
        """
        if char not in self.tape_symbols:
            raise ValueError(f"{char} not a valid tape symbol")
        n = self.head
        if n < 0:
            raise ValueError("Cannot write to left of first cell")
        if not self.tape:
            raise ValueError("Input not yet provided to Turing Machine")
        self.tape = self.tape[:n] + char + self.tape[n+1:]

    def run(self, max_steps=10000, verbose=False, steps=None):
        """
        Run the Turing Machine until halting or reaching max_steps.

        Parameters
        ----------
        max_steps   Maximum number of steps to execute
        verbose     Print tape state after each step
        steps       'keys' for keypress stepping, or float for timed delay

        Returns
        -------
        str 'valid' if halted within max_steps, 'invalid' otherwise
        """
        num_steps = 0
        while num_steps < max_steps:
            num_steps += 1
            result = self.step()
            if verbose:
                print(self.get_tape_contents(False))
                print(' ' * self.head + '-')
                print(self.current_state, self.head)
            if steps == 'keys':
                input('')
            elif isinstance(steps, (float, int)):
                import time
                time.sleep(steps)
            if not result:
                return 'valid'
        return 'invalid'

    def step(self) -> bool:
        """
        Execute one step of the Turing Machine.

        Returns
        -------
        bool True if step executed, False if in halt state
        """
        if self.current_state in self.halt_states:
            return False
        current_symbol = self.read_tape()
        k = Rule.make_hash(self.current_state, current_symbol)
        if k not in self.rules.keys():
            raise ValueError("Rule not defined for the current state and symbol")

        this_rule = self.rules[k]
        self.write_tape(this_rule.write_symbol)
        self.head += 1 if this_rule.direction == 'R' else -1
        self.current_state = this_rule.next_state
        return True

    def get_tape_contents(self, strip=True):
        """
        Get the contents of the tape.

        Parameters
        ----------
        strip   Remove blank symbols from tape edges

        Returns
        -------
        str Contents of the tape
        """
        if not self.tape or not isinstance(self.tape, str):
            raise ValueError("Input not yet provided to Turing Machine")
        if strip:
            return self.tape.strip(self.blank_symbol)
        return self.tape

def create_binary_doubler_tm() -> TuringMachine:
    """
    Create a Turing Machine that doubles a binary number.

    Returns
    -------
    TuringMachine   A Turing Machine that doubles a binary number
    """
    rules = [
        Rule(1, '1', '1', 1, 'R'),
        Rule(1, '0', '0', 1, 'R'),
        Rule(1, ' ', '0', 2, 'R'),
    ]
    tm = TuringMachine(rules, '10', '10 ', ' ', 1, [2])
    return tm

def test_binary_doubler():
    print("TESTING BINARY DOUBLER")
    test_vals = [
        1,
        5,
        15,
        172,
        976531,
        10123,
        132578967132576
    ]
    for test_val in test_vals:
        tm = create_binary_doubler_tm()
        test_input = bin(test_val)[2:]
        tm.set_input(test_input)
        tm.run()
        res = tm.get_tape_contents()
        test_result = int(res, 2)
        if test_result == test_val * 2:
            print('SUCCESS: ', end='')
        else:
            print('FAILURE:', end='')
        print(test_input, ' -> ', res, '  |  ', test_val, '* 2 =', test_result)
    print()

def create_string_reverser_tm():
    """
    Create a Turing Machine that reverses a string of 'a' and 'b' characters.

    Returns
    -------
    TuringMachine   A Turing Machine that reverses a string of 'a' and 'b'
    """
    a = 'a'
    b = 'b'
    x = 'X'
    r = 'R'
    l = 'L'
    sp = '^'

    rules = [
        Rule(1, a, 'A', 2, r),
        Rule(1, b, 'B', 2, r),

        Rule(2, x, x, 2, r),
        Rule(2, b, b, 2, r),
        Rule(2, a, a, 2, r),
        Rule(2, sp, sp, 3, l),

        Rule(3, x, x, 3, l),
        Rule(3, a, x, 4, r),
        Rule(3, b, x, 6, r),
        Rule(3, 'A', sp, 8, r),
        Rule(3, 'B', sp, 9, r),

        Rule(4, x, x, 4, r),
        Rule(4, a, a, 4, r),
        Rule(4, b, b, 4, r),
        Rule(4, sp, a, 5, l),

        Rule(5, a, a, 5, l),
        Rule(5, b, b, 5, l),
        Rule(5, x, x, 3, l),

        Rule(6, x, x, 6, r),
        Rule(6, a, a, 6, r),
        Rule(6, b, b, 6, r),
        Rule(6, sp, b, 7, l),

        Rule(7, a, a, 7, l),
        Rule(7, b, b, 7, l),
        Rule(7, x, x, 3, l),

        Rule(8, x, sp, 8, r),
        Rule(8, a, a, 8, r),
        Rule(8, b, b, 8, r),
        Rule(8, sp, a, 10, l),

        Rule(9, x, sp, 9, r),
        Rule(9, a, a, 9, r),
        Rule(9, b, b, 9, r),
        Rule(9, sp, b, 10, l),
    ]
    return TuringMachine(rules, 'ab', 'abABX^', '^', 1, [10])

def test_string_reverser():
    print("TESTING STRING REVERSER")
    test_strings = [
        'a',
        'b',
        'aa',
        'bb',
        'aba',
        'bab',
        'aab',
        'baa',
        'aaaaaab',
        'bbbaaab',
        'baaabbba',
        'baaaaaabb',
    ]

    for test_s in test_strings:
        tm = create_string_reverser_tm()
        tm.set_input(test_s)
        tm.run()
        if tm.get_tape_contents() == test_s[::-1]:
            print('SUCCESS: ', end='')
        else:
            print('FAILURE: ', end='')
        print(test_s, ' -> ', tm.get_tape_contents())
    print()

if __name__ == '__main__':
    test_binary_doubler()
    test_string_reverser()
