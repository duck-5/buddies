from dataclasses import dataclass
import json
from datetime import datetime, timedelta
import os
from typing import Any, Dict
from agent.tools.tool_interface import Tool

@dataclass
class AddEventToolConfig:
    event_files_path: str

class AddEventTool(Tool):
    NAME="add_event"
    DESCRIPTION="Creates an event with time, notification, importance, and description fields. The time field can be a specific datetime or a duration from now. Datetime is in the format dd/mm/yyyy hh:mm. Duration is in the format HH:MM:SS."
    INPUT_FORMAT='{"time": "str", "notification": "bool", "importance": "int", "description": "str"}'

    def __init__(self, config: AddEventToolConfig) -> None:
        super().__init__(config)
    
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
            if not importance.isnumeric():
                return "Error: 'importance' must be a number."
            
            importance = int(importance)
            
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
        file_path = self.config.event_files_path
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

    def _parse_time(self, time_input: str) -> str:
        """Parses the time input and returns an ISO 8601 formatted string."""
        try:
            # Check if input is a specific date and time
            try:
                return datetime.strptime(time_input, "%d/%m/%Y %H:%M").isoformat()
            except ValueError:
                pass

            # Check if input is a relative time (e.g., 03:30:00)
            try:
                relative_time = datetime.now() + timedelta(seconds=self._parse_duration(time_input))
                return relative_time.isoformat()
            except ValueError:
                pass

            raise ValueError("Invalid time format. Use 'dd/mm/yyyy hh:mm' or a duration like 'HH:MM:SS'.")
        except Exception as e:
            raise ValueError(f"Failed to parse time: {e}")