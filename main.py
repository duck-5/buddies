from agent.agent_system import Config, logger, AgentParser
from agent.io import MockLLMClient

def main():
    try:
        config = Config()
    except FileNotFoundError:
        logger.critical("Configuration file 'agent_config.toml' not found.")
        return

    logger.info(f"Scanning for tools in '{config.plugins_dir}'...")
    
    parser = AgentParser(config)
    
    logger.info("System initialized. Generating system prompt...")
    system_prompt = parser.get_system_prompt()

    # Initialize mock LLM client with the existing mock response
    mock_response = """
    {
        "thought": "Adding milk using defaults.",
        "tool_calls": [
            {
                "tool_name": "add_to_list",
                "arguments": {
                    "list_name": "groceries",
                    "item": "2milk"
                }
            }
        ]
    }
    """
    llm_client = MockLLMClient(config={"response": mock_response.strip()})
    
    # Simulate user message
    user_message = "Add milk to my groceries list"
    
    logger.info("Calling LLM...")
    llm_response = llm_client.call(system_prompt, user_message)
    
    logger.info("Processing LLM response...")
    results = parser.parse_and_execute(llm_response)
    
    logger.info("Execution Results:")
    for res in results:
        logger.info(res)

if __name__ == "__main__":
    main()