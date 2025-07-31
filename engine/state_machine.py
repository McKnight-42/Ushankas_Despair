import json

class ChatStateMachine:
    def __init__(self, script_path="responses/scripts.json"):
        with open(script_path, 'r') as f:
            self.dialogue = json.load(f)
        self.state = "intro"
        self.context = {}

    def get_current_text(self):
        node = self.dialogue[self.state]
        text = node["text"]
        if "{name}" in text and "name" in self.context:
            return text.format(name=self.context["name"])
        return text


    def advance(self, user_input: str):
        node = self.dialogue[self.state]

        if node.get("input") == "store_name":
            self.context["name"] = user_input
            self.state = node["next"]
            return

        if "options" in node:
            normalized = user_input.strip().lower()
            if normalized in node["options"]:
                self.state = node["options"][normalized]
            else:
                print("System: That wasn't one of the choices...")
        else:
            self.state = node.get("next", None)

