
from agent.agent_system import Config, logger, AgentParser

import logging
from agent.agent_system import Config, AgentParser
from agent.llm import GeminiClient

logger = logging.getLogger(__name__)


def main():
    try:
        config = Config()
    except FileNotFoundError:
        logger.critical("Configuration file 'agent_config.toml' not found.")
        return

    parser = AgentParser(config)
    
    logger.info("System initialized. Generating system prompt...")
    system_prompt = parser.get_system_prompt()



    # Simulate LLM output
    mock_response = """
    {
        "thought": "Adding milk using defaults.",
        "tool_calls": [
            {
                "tool_name": "add_to_list",
                "arguments": {
                    "list_name": "invite_list",
                    "item": "Not Dikla"
                }
            },
            {
                "tool_name": "add_event",
                "arguments": {
                    "time": "10/10/2024 10:00",
                    "description": "Doctor's appointment",
                    "importance": "1",
                    "notification": true
                    
                }
            }
        ]
    }
    """

    API_KEY = "AIzaSyBMNdN7CRw619o7HKHJ-xlFcmREskGhbkk"
    llm_client = GeminiClient(config={"api_key": API_KEY})
    
    # Simulate user message
    user_message = "I ran out of milk"
    
    logger.info("Calling LLM...")
    llm_response = llm_client.call(system_prompt, user_message)
    
    logger.info("Processing LLM response...")
    results = parser.parse_and_execute(llm_response)
    
    logger.info("Execution Results:")
    for res in results:
        logger.info(res)

if __name__ == "__main__":
    main()