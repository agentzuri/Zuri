import random
import json

class AgentZuri:
    def __init__(self):
        with open('knowledge_base.json', 'r') as file:
            self.knowledge_base = json.load(file)
        
        self.name = "Zuri"

    def respond(self, user_input):
        """
        Generate a response based on the user input.
        This is a very simplified version where responses are matched against keywords.
        """
        for question, answer in self.knowledge_base.items():
            if any(keyword in user_input.lower() for keyword in question.split()):
                return answer
        
        return self.default_response()

    def default_response(self):
        """Provide a default response when no match is found."""
        responses = [
            "I'm not sure I understand that. Could you rephrase?",
            "That's an interesting question! Let me think about it...",
            "Hmm, I'll need to learn more about that. Can you tell me more?"
        ]
        return random.choice(responses)

    def run(self):
        """Main loop for interacting with the user."""
        print(f"Hello! I'm {self.name}, how can I assist you today?")
        
        while True:
            user_input = input("You: ").lower()
            if user_input in ['exit', 'quit', 'bye']:
                print(f"{self.name}: Goodbye!")
                break
            response = self.respond(user_input)
            print(f"{self.name}: {response}")

if __name__ == "__main__":
    zuri = AgentZuri()
    zuri.run()
