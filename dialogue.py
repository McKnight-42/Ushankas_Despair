from responses.static import get_response

def start_chat():
    while True:
        user_input = input("> ").strip().lower()

        if user_input in ("exit", "quit"):
            print("System: Goodbye.")
            break

        response = get_response(user_input)
        print(f"System: {response}")
