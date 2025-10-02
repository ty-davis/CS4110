# Name: Ty Davis
# Student ID: W01367741
# Date: 10/1/2025

def is_in_language_L(string):
    """
    Check if a string belongs to language L = {a^n b^n | n >= 1}
    
    Args:
        string (str): Input string to check
    
    Returns:
        bool: True if string is in L, False otherwise
    
    Examples:
        is_in_language_L("ab") -> True
        is_in_language_L("aabb") -> True  
        is_in_language_L("aaabbb") -> True
        is_in_language_L("aba") -> False
        is_in_language_L("") -> False
    """
    # count all the a's and b's
    num_as = string.count('a')
    num_bs = string.count('b')

    # ensure there are an equal number greater than 0
    if num_as != num_bs or num_as == 0:
        return False

    # make sure no a's are present in the second half of the string
    if 'a' in string[num_as:]:
        return False

    # default case
    return True

def kleene_closure_generator(base_language, max_length):
    """
    Generate all strings in L* (Kleene closure) up to max_length
    
    Args:
        base_language (list): List of strings representing the base language
        max_length (int): Maximum length of generated strings
    
    Returns:
        set: Set of all strings in L* with length <= max_length
    
    Example:
        kleene_closure_generator(["a", "bb"], 4) should include:
        - "" (empty string, always in L*)
        - "a", "bb" (from L¹)
        - "aa", "abb", "bba", "bbbb" (from L²)
        - etc.
    """
    final = set([''])
    for _ in range(max_length):
        # for each layer
        for string in base_language:
            small_set = set()
            for item in final:
                small_set.add(string + item)
            final = final.union(small_set)
    return final


def generate_recursive_language_M(n):
    """
    Generate the nth string in language M using recursive definition
    
    Args:
        n (int): Depth of recursion (0 = base case)
    
    Returns:
        str: The string generated at recursion depth n
    
    Examples:
        generate_recursive_language_M(0) -> "x"
        generate_recursive_language_M(1) -> "yxz"
        generate_recursive_language_M(2) -> "yyxzz"
        generate_recursive_language_M(3) -> "yyyxzzz"
    """
    return "y" + generate_recursive_language_M(n-1) + "z" if n > 0 else "x"


def regex_match(pattern, string):
    """
    Check if string matches the given regular expression pattern
    Support basic operations: concatenation, | (union), * (Kleene star)
    
    Args:
        pattern (str): Regular expression pattern
        string (str): String to match against pattern
    
    Returns:
        bool: True if string matches pattern, False otherwise
    
    Supported patterns:
        - Single characters: 'a' matches "a"
        - Union: 'a|b' matches "a" or "b"  
        - Kleene star: 'a*' matches "", "a", "aa", "aaa", etc.
        - Concatenation: 'ab' matches "ab"
        - Combined: 'a*b|c' matches strings of a's followed by b, or just c
    
    Examples:
        regex_match("a*", "aaa") -> True
        regex_match("a*b", "aab") -> True
        regex_match("a|b", "a") -> True
        regex_match("a|b", "c") -> False
    """
    if "|*" in pattern:
        raise Exception("Bad pattern. '|*' can not be present")
    if pattern.startswith("*"):
        raise Exception("Bad pattern. Cannot start pattern with '*'.")

    # final variable used to keep track of whether it matches
    does_match = False

    # split up the unions
    pats = pattern.split('|')
    for pat in pats:
        is_matching = True

        # in here, there is only concatenation and the kleene *
        i = 0
        blocks = []
        while i < len(pat):
            # look for * if not the last character
            # to build the blocks
            if i != len(pat) - 1 and pat[i+1] == '*':
                blocks.append((pat[i], True)) # True because has Kleene star
                i += 2
            else:
                blocks.append((pat[i], False)) # False because no Kleene star
                i += 1


        b_ptr = 0
        for char in string:
            if b_ptr >= len(blocks):
                is_matching = False
                break

            # find all valid chars based on b_ptr
            keep_looking = True
            valid = []
            diff = 0
            while keep_looking:
                if b_ptr + diff == len(blocks):
                    break

                valid.append(blocks[b_ptr + diff][0])
                keep_looking = blocks[b_ptr + diff][1] # does this have Kleene *
                diff += 1

            first_match = -1
            for i, v in enumerate(valid):
                if char == v:
                    first_match = i
                    break

            if first_match < 0:
                is_matching = False

            if blocks[b_ptr][1]: # if this one is Kleene *
                b_ptr += first_match
                if not blocks[b_ptr][1]: # if that one is not Kleene *
                    b_ptr += 1

            else:
                b_ptr += 1

        if is_matching:
            # we got through all the chars in the string but there
            # may still be another block to evaluate
            remaining = [x[1] for x in blocks[b_ptr:]]
            does_match = all(remaining)

    return does_match




def test_assignment():
    # Test Task 1: Language L membership
    assert is_in_language_L("ab") == True
    assert is_in_language_L("aabb") == True
    assert is_in_language_L("aaabbb") == True
    assert is_in_language_L("aabbb") == False
    assert is_in_language_L("aba") == False
    assert is_in_language_L("") == False
    assert is_in_language_L("a") == False
    assert is_in_language_L("b") == False
    
    # Test Task 2: Kleene closure
    result = kleene_closure_generator(["a"], 3)
    expected = {"", "a", "aa", "aaa"}
    assert result == expected
    
    result2 = kleene_closure_generator(["ab"], 4)
    assert "" in result2
    assert "ab" in result2
    assert "abab" in result2
    assert len([s for s in result2 if len(s) <= 4]) >= 3
    
    # Test Task 3: Recursive language
    assert generate_recursive_language_M(0) == "x"
    assert generate_recursive_language_M(1) == "yxz"
    assert generate_recursive_language_M(2) == "yyxzz"
    assert generate_recursive_language_M(3) == "yyyxzzz"
    
    # Test Task 4: Regular expressions
    assert regex_match("a*", "") == True
    assert regex_match("a*", "aaa") == True
    assert regex_match("a*b", "aaab") == True
    assert regex_match("a|b", "a") == True
    assert regex_match("a|b", "c") == False
    assert regex_match("ab", "ab") == True
    assert regex_match("ab", "a") == False
    
    print("All tests passed!")

def main():
    print("-----------------START NEW-----------------")
    print(regex_match("ab*c*d", "ad"))

    print("-----------------START NEW-----------------")
    print(regex_match("ab*c*d", "abcd"))

    print("-----------------START NEW-----------------")
    print(regex_match("ab*c*d", "ade"))

    print("-----------------START NEW-----------------")
    print(regex_match("ab*c*d", "acd"))

    print("-----------------START NEW-----------------")
    print(regex_match("ab*c*d", "abbbbd"))

    print("-----------------START NEW-----------------")
    print(regex_match("ab*c*d", "a"))

if __name__ == "__main__":
    # main()
    test_assignment()
