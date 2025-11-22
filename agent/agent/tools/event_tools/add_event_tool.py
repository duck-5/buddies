import json
from datetime import datetime, timedelta
import os
from typing import Any, Dict
from agent.tools.tool_interface import Tool

class AddEventTool(Tool):
    NAME="event_creator"
    DESCRIPTION="Creates an event with time, notification, importance, and description fields."
    INPUT_FORMAT='{"time": "str", "notification": "bool", "importance": "int", "description": "str"}'

    def execute(self, arguments_json: str) -> Any:
        try:
            args = json.loads(arguments_json)

            # Parse time field
            time_input = args.get("time")
            event_time = self._parse_time(time_input)

            # Extract other fields
            notification = args.get("notification", False)
            importance = args.get("importance", 1)
            description = args.get("description", "")

            if not description:
                return "Error: 'description' is required."

            # Validate importance
            if not (1 <= importance <= 5):
                return "Error: 'importance' must be between 1 and 5."

            # Create event
            event = {
                "time": event_time,
                "notification": notification,
                "importance": importance,
                "description": description,
            }

            # Save event to file
            self._save_event(event)

            return {"status": "success", "event": event}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _save_event(self, event: Dict[str, Any]) -> None:
        file_path = self.config.get("events_file_path", "events.json")
        events = []

        # Load existing events if the file exists
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    events = json.load(f)
                except json.JSONDecodeError:
                    pass

        # Append the new event
        events.append(event)

        # Save back to the file
        with open(file_path, "w") as f:
            json.dump(events, f, indent=2)

    def _parse_duration(self, duration: str) -> int:
        """Parses a duration string (HH:MM:SS) into total seconds."""
        try:
            hours, minutes, seconds = map(int, duration.split(":"))
            return hours * 3600 + minutes * 60 + seconds
        except Exception as e:
            raise ValueError(f"Invalid duration format: {e}")