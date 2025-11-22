import json
from typing import Any, Dict, List
from agent.parser import AgentParser, Config
from agent.config import GOOGLE_API_KEY
from agent.llm.gemini_client import GeminiClient, GeminiConfig

class AgentFlow:
    """Main flow of the system encapsulated in a class."""

    def __init__(self, parser: AgentParser, llm_client: GeminiClient):
        self.parser = parser
        self.llm_client = llm_client
        self.notes: List[str] = []

    def add_note(self, note: str):
        """Add a special note to the list of notes."""
        self.notes.append(note)

    def main_flow(self):
        """Main flow of the system."""
        while True:
            # Step 1: Get user input
            user_input = input("Enter your input: ")
            self.basic_flow(user_input)
    
    def basic_flow(self, user_input: str):
        while True:
            # Step 2: Add notes from the list
            if self.notes:
                notes_text = "\n".join(f"[NOTE]: {note}" for note in self.notes)
                user_input += f"\n{notes_text}"
                self.notes.clear()  # Clear notes after including them

            # Step 3: Pass input to LLM
            system_prompt = self.parser.get_system_prompt()
            llm_response = self.llm_client.call(system_prompt, user_input)

            # Step 4: Parse and execute LLM output
            results = self.parser.parse_and_execute(llm_response)

            # Step 5: Handle results
            if results:
                self.notes += "Tools were invoked. The output hasn't passed to the user. Make sure that all tools were invoked properly, and then the output will be returned to the user."
                self.return_results_to_llm(results)
            else:
                # Call output function if no tools were invoked
                print("========\n", llm_response, "\n========")
                parsed_output = json.loads(llm_response)
                output_text = parsed_output.get("response", "")
                self.call_output_function(output_text)
                return

    def return_results_to_llm(self, results: List[Dict[str, Any]]):
        """Send tool execution results back to the LLM."""
        try:
            # Format the results as a JSON string
            results_json = json.dumps({"tool_results": results}, indent=2)
            print("Returning results to LLM:")
            print(results_json)

            # Optionally, you can send the results back to the LLM client if needed
            # self.llm_client.send_results(results_json)
        except Exception as e:
            self.llm_client.logger.error(f"Failed to return results to LLM: {e}")

    def call_output_function(self, output_text: str):
        """Simulates calling an output function with the LLM's text."""
        print("Output:", output_text)

if __name__ == "__main__":
    # Initialize configuration and parser
    config = Config()
    parser = AgentParser(config)

    # Initialize GeminiClient
    gemini_config = GeminiConfig(
        api_key = GOOGLE_API_KEY,
        chat_mode=True
    )
    
    llm_client = GeminiClient(gemini_config)

    # Create and run the agent flow
    agent_flow = AgentFlow(parser, llm_client)
    agent_flow.main_flow()