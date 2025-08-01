import re

def extract_name(user_input: str) -> str:
    """
    Attempt to extract a name from user input by removing
    common intro phrases and taking the first remaining word.
    """

    cleaned = user_input.lower()
    cleaned = re.sub(r"\b(i'?m|i am|my name is|it's|it is)\b", "", cleaned)
    cleaned = cleaned.strip(" ,.!?\"'")
    words = cleaned.split()

    if words:
        return words[0].capitalize()
    else:
        return "Hello Stranger"

def parse_triggers(user_input: str, context: dict) -> dict:
    """
    Detect and act on simple global triggers.
    Returns possibly-updated context.
    """
    ui = user_input.strip().lower()

    if "help" in ui:
        context["wants_help"] = True

    if any(word in ui for word in ["scared", "afraid", "nervous", "uneasy"]):
        context["emotion"] = "fear"

    if "name" not in context:
        # If the user responds to a name prompt, attempt to pull a name
        # Simple heuristic: if input looks like a name phrase or is short
        if re.search(r"i[' ]?m |my name is |call me ", user_input.lower()) or len(user_input.split()) <= 2:
            context["name"] = extract_name(user_input)

    return context
