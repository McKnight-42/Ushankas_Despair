import json
from engine.triggers import parse_triggers, extract_name

def resolve_choice(user_input: str, valid_options: dict, context: dict) -> str | None:
    """
    Lightweight choice resolution: exact first, then substring matching for common variants.
    NLP layer will replace/augment this later.
    """
    normalized = user_input.strip().lower()

    if normalized in valid_options:
        return valid_options[normalized]

    for key in valid_options:
        if key == "yes" and any(token in normalized for token in ["yes", "y", "yeah", "yep", "sure"]):
            return valid_options[key]
        if key == "no" and any(token in normalized for token in ["no", "nah", "nope"]):
            return valid_options[key]

    return None


class ChatStateMachine:
    def __init__(self, script_path="responses/scripts.json"):
        """
        Initialize the state machine with the dialogue script.
        """
        with open(script_path, 'r') as f:
            self.dialogue = json.load(f)
        self.state = "intro"
        self.context = {}

    def get_current_text(self):
        """
        Retrieve the current state's dialogue text,
        substituting any placeholders from context.
        """
        node = self.dialogue[self.state]
        text = node["text"]
        if "{name}" in text and "name" in self.context:
            return text.format(name=self.context["name"])
        return text

    def advance(self, user_input: str):
        """
        Advance the state machine based on user input,
        handling special inputs, triggers, and branching.
        """
        node = self.dialogue[self.state]

        # 1. Handle input nodes like storing name
        if node.get("input") == "store_name":
            self.context["name"] = extract_name(user_input)
            self.state = node["next"]
            return

        # 2. Handle special cases like help or fear
        self.context = parse_triggers(user_input, self.context)

        if self.context.get("wants_help") and self.state != "help_response":
            self.state = "help_response"
            return

        if self.context.get("emotion") == "fear":
            if "fear_response" in self.dialogue:
                self.state = "fear_response"
                return

        if "options" in node:
            resolved = resolve_choice(user_input, node["options"], self.context)
            if resolved:
                self.state = resolved
            else:
                print("System: That wasn't one of the choices...")
        else:
            self.state = node.get("next", None)

