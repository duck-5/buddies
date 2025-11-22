from dataclasses import dataclass
import json
import os
from typing import Any, Dict
from agent.tools.tool_interface import Tool

@dataclass
class RemoveEventToolConfig:
    events_file_path: str

class RemoveEventTool(Tool):
    NAME="remove_event"
    DESCRIPTION="Removes an event from the 'events.json' file based on a unique identifier or description."
    INPUT_FORMAT='{"description": "str"}'

    def execute(self, arguments_json: str) -> Any:
        try:
            args = json.loads(arguments_json)
            description = args.get("description")

            if not description:
                raise "Error: 'description' is required."

            file_path = self.config.get("events_file_path", "events.json")

            # Check if the file exists
            if not os.path.exists(file_path):
                raise "No events file found."

            # Load existing events
            with open(file_path, "r") as f:
                try:
                    events = json.load(f)
                except json.JSONDecodeError:
                    raise "Failed to parse events file."

            # Filter out the event with the matching description
            updated_events = [event for event in events if event.get("description") != description]

            # Check if any event was removed
            if len(updated_events) == len(events):
                raise "No matching event found."

            # Save the updated events back to the file
            with open(file_path, "w") as f:
                json.dump(updated_events, f, indent=2)

            return "Event removed successfully."

        except Exception as e:
            raise e