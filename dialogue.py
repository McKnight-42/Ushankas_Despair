import random
import time

from engine.state_machine import ChatStateMachine
from effects.typewriter import typewriter_print
from effects.char_glitch import glitch_text
from effects.mirror import maybe_mirror_input

def extract_echoable_word(past_inputs):
    """
    Pick a random word from earlier user inputs to echo back.
    """
    flat = []
    for ui in past_inputs:
        flat.extend([w.strip(".,!?\"'") for w in ui.split() if w])
    if not flat:
        return None
    return random.choice(flat)

def start_chat():
    sm = ChatStateMachine()
    user_history = []

    while sm.state:
        # Simulate "thinking" pause before replying
        time.sleep(random.uniform(0.6, 1.4))

        # Occasionally echo something from earlier inputs for unsettling effect
        if user_history and random.random() < 0.08:
            word = extract_echoable_word(user_history)
            if word:
                typewriter_print(f"System: ...you said '{word}', didn't you?")
                time.sleep(0.4)

        current_text = sm.get_current_text()

        if sm.state == "glitch_hint":
            current_text = glitch_text(current_text)

        typewriter_print(f"System: {current_text}")

        if random.random() < 0.3:
            time.sleep(random.uniform(0.3, 0.8))

        user_input = input("> ")

        echoed = maybe_mirror_input(user_input)
        if echoed != user_input:
            print(f"System: ...{echoed}")

        if user_input.lower() in ("exit", "quit"):
            print("System: You can't leave that easily.")
            break

        user_history.append(user_input)

        sm.advance(user_input)
