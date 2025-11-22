from agent.agent.parser import AgentParser, Config
from agent.agent.config import GOOGLE_API_KEY
from agent.agent.flow import AgentFlow
from agent.agent.llm.gemini_client import GeminiClient, GeminiConfig
from threading import Thread
from buddy.events_handler import pool_events_handler

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
    Thread(target=agent_flow.main_flow).start()
    Thread(target=pool_events_handler, args=(agent_flow,)).start()