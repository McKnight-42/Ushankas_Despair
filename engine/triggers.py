import re

def extract_name(user_input: str) -> str:
    """
    Try to pull a name out of free-form input like:
      "I'm John", "My name is Alice", "Call me Sam"
    Falls back to the first capitalized word or the raw input.
    """
    patterns = [
        r"i(?:'| a)?m\s+([A-Za-z]+)",        # I'm John / Im John / I am John
        r"my name is\s+([A-Za-z]+)",        # my name is John
        r"call me\s+([A-Za-z]+)",           # call me John
    ]
    lowered = user_input.lower()
    for pattern in patterns:
        match = re.search(pattern, lowered)
        if match:
            return match.group(1).capitalize()

    first = user_input.strip().split()[0]
    cleaned = re.sub(r"[^\w\-']", "", first)
    return cleaned.capitalize()

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
