from agent.agent_system import Config, logger, AgentParser

def main():
    try:
        config = Config()
    except FileNotFoundError:
        logger.critical("Configuration file 'agent_config.toml' not found.")
        return

    logger.info(f"Scanning for tools in '{config.plugins_dir}'...")
    
    parser = AgentParser(config)
    
    logger.info("System initialized. Generating system prompt...")
    # print(parser.get_system_prompt()) # Uncomment to see prompt

    # Simulate LLM output
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
    
    logger.info("Simulating LLM Response processing...")
    results = parser.parse_and_execute(mock_response)
    
    logger.info("Execution Results:")
    for res in results:
        logger.info(res)

if __name__ == "__main__":
    main()