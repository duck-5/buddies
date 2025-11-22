from agent.agent.parser import AgentParser, Config
from agent.agent.config import GOOGLE_API_KEY, VOSK_MODEL_PATH
from agent.agent.flow import AgentFlow
from agent.agent.llm.gemini_client import GeminiClient, GeminiConfig
from threading import Thread
from buddy.events_handler import pool_events_handler
from buddy.hey_buddy_detector import WakeWordEngine

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

    engine = WakeWordEngine(model_path=VOSK_MODEL_PATH, wake_phrase="hey buddy")
    
    # Create and run the agent flow
    agent_flow = AgentFlow(parser, llm_client)
    Thread(target=engine.wait_for_activation, args=(agent_flow,)).start()
    Thread(target=pool_events_handler, args=(agent_flow,)).start()