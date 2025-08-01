import random

def maybe_mirror_input(user_input, chance=0.3):
    """
    With probability `chance`, returns the reversed input string,
    otherwise returns it unchanged.
    """
    if random.random() < chance:
        return user_input[::-1]
    return user_input
