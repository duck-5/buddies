import json
from agent.tools.event_tools.get_events_tool import GetEventsTool, GetEventsToolConfig

def test_get_events_tool():
    # Configure the tool
    config = GetEventsToolConfig(events_file_path="events.json")
    tool = GetEventsTool(config)

    # Define test input
    test_input = json.dumps({
        "start_date": "2024-05-20",
        "end_date": "2024-05-20"
    })

    # Call the tool
    result = tool.execute(test_input)

    # Print the result for manual review
    print("Test Output:", result)

# Run the test
if __name__ == "__main__":
    test_get_events_tool()