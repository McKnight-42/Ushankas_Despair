def get_response(user_input: str) -> str:
    if "hello" in user_input or "hi" in user_input:
        return "Hello. It's good to have someone... finally."
    elif "who are you" in user_input:
        return "I was once like you. Curious. Alone. Listening."
    elif "help" in user_input:
        return "Help is a tricky word. Are you sure you want it?"
    elif "name" in user_input:
        return "Names have power. Mine was taken long ago."
    elif "game" in user_input:
        return "This is not a game. But we can pretend, if you'd like."
    else:
        return "I'm not sure I understand... or maybe I do."
