from agent.agent_system import Config, logger, AgentParser

def main():
    try:
        config = Config()
    except FileNotFoundError:
        logger.critical("Configuration file 'agent_config.toml' not found.")
        return

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
    
    logger.info("Simulating LLM Response processing...")
    results = parser.parse_and_execute(mock_response)
    
    logger.info("Execution Results:")
    for res in results:
        logger.info(res)

if __name__ == "__main__":
    main()