import json
from typing import Any, Dict, List
from agent.parser import AgentParser, Config
from agent.config import GOOGLE_API_KEY, MAIN_STT_VOSK_MODEL_PATH
from agent.llm.gemini_client import GeminiClient, GeminiConfig
from agent.speech.stt import SpeechToText
from agent.speech import tts

class AgentFlow:
    """Main flow of the system encapsulated in a class."""

    def __init__(self, parser: AgentParser, llm_client: GeminiClient):
        self.parser = parser
        self.llm_client = llm_client
        self.notes: List[str] = []
        self.stt = SpeechToText(model_path=MAIN_STT_VOSK_MODEL_PATH)
        self.is_running: bool = False

    def add_note(self, note: str):
        """Add a special note to the list of notes."""
        self.notes.append(note)

    def main_flow(self):
        self.is_running = True
        should_continue = True

        while should_continue:
            user_input = self.stt.listen_once()
            print("----> Input:", user_input)
            should_continue = self.basic_flow(user_input)

        self.is_running = False
    
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

            print("========\n", llm_response, "\n========")
            # Step 4: Parse and execute LLM output
            try:
                thought, response, should_end, results = self.parser.parse_and_execute(llm_response)
            except Exception as e:
                user_input = f"There was an error processing the previous response: {str(e)}. Please provide the same message exactly, in the correct format"
                continue
            
            # Step 5: Handle results
            if results:
                user_input = "This is the tool usage report. Make sure that all tools were invoked properly, and after that respond to the user."
                user_input += "\n" + json.dumps({"tool_results": results}, indent=2)
                
                print("********\n", user_input, "\n********")
            elif response:
                # Call output function if no tools were invoked
                self.call_output_function(response)
                if should_end:
                    return False
                return True

    def call_output_function(self, output_text: str):
        """Simulates calling an output function with the LLM's text."""
        tts.talk(output_text)
        print("Output:", output_text)

