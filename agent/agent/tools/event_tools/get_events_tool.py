import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from agent.tools.tool_interface import Tool
from dataclasses import dataclass

logger = logging.getLogger("Tools.GetEvents")

@dataclass
class GetEventsToolConfig:
    event_files_path: str

class GetEventsTool(Tool):
    NAME = "get_events"
    DESCRIPTION = "Retrieves events by title or date range."
    INPUT_FORMAT = '{"title": "str (optional)", "start_date": "str (optional, format: YYYY-MM-DD)", "end_date": "str (optional, format: YYYY-MM-DD)"}'

    def __init__(self, config: GetEventsToolConfig) -> None:
        super().__init__(config)
        self.event_files_path = config.event_files_path

    def _load_data(self) -> List[Dict[str, Any]]:
        """Load events from the file."""
        try:
            with open(self.event_files_path, "r") as file:
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
            title: Optional[str] = args.get("title")
            start_date: Optional[str] = args.get("start_date")
            end_date: Optional[str] = args.get("end_date")

            # Load the events data
            data = self._load_data()

            # Filter events by title if provided
            if title:
                data = [event for event in data if title.lower() in event["title"].lower()]

            # Filter events by date range if provided
            if start_date:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                data = [event for event in data if datetime.strptime(event["date"], "%Y-%m-%d") >= start_date_obj]

            if end_date:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
                data = [event for event in data if datetime.strptime(event["date"], "%Y-%m-%d") <= end_date_obj]

            logger.info("Retrieved events based on the provided criteria.")
            return data

        except Exception as e:
            logger.error(f"Error in get_events: {e}")
            raise
