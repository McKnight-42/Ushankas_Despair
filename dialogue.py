from engine.state_machine import ChatStateMachine

def start_chat():
    sm = ChatStateMachine()

    while sm.state:
        print(f"System: {sm.get_current_text()}")
        user_input = input("> ")
        if user_input.lower() in ("exit", "quit"):
            print("System: You can't leave that easily.")
            break
        sm.advance(user_input)
