import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from agent.tools.tool_interface import Tool
from dataclasses import dataclass
from .models import Event

logger = logging.getLogger("Tools.GetEvents")

@dataclass
class GetEventsToolConfig:
    events_file_path: str

class GetEventsTool(Tool):
    NAME = "get_events"
    DESCRIPTION = "Retrieves events by date range."
    INPUT_FORMAT = '{"start_date": "str (optional, format: YYYY-MM-DD)", "end_date": "str (optional, format: YYYY-MM-DD)"}'

    def __init__(self, config: GetEventsToolConfig) -> None:
        super().__init__(config)
        self.events_file_path = config.events_file_path

    def _load_data(self) -> List[Dict[str, Any]]:
        """Load events from the file."""
        try:
            with open(self.events_file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except Exception as e:
            logger.error(f"Failed to load events: {e}")
            raise

    def execute(self, arguments_json: str) -> Any:
        try:
            # Parse the input arguments
            args = json.loads(arguments_json)
            start_date: Optional[str] = args.get("start_date")
            end_date: Optional[str] = args.get("end_date")

            # Load the events data
            data = self._load_data()
            data = [Event(**event) for event in data]

            # Filter events by date range if provided
            if start_date:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                data = [event for event in data if datetime.fromisoformat(event.time) >= start_date_obj]

            if end_date:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
                data = [event for event in data if datetime.fromisoformat(event.time) <= end_date_obj]

            logger.info("Retrieved events based on the provided criteria.")
            return data

        except Exception as e:
            logger.error(f"Error in get_events: {e}")
            raise
