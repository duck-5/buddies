import json
import logging
from typing import Any
from agent.tools.list_tools.file_based_list_tool import FileBasedListTool, FileBasedListToolConfig

logger = logging.getLogger("Tools.GetListsHeaders")

class GetListsHeadersTool(FileBasedListTool):
    NAME = "get_lists_headers"
    DESCRIPTION = "Retrieves the headers of all lists in the system."
    INPUT_FORMAT = "{}"  # No input required

    def __init__(self, config: FileBasedListToolConfig) -> None:
        super().__init__(config)

    def execute(self, arguments_json: str) -> Any:
        try:
            # Load the data from the file
            data = self._load_data()

            # Extract the headers (list names)
            headers = list(data.keys())

            logger.info("Retrieved list headers.")
            return headers

        except Exception as e:
            logger.error(f"Error in get_lists_headers: {e}")
            raise
