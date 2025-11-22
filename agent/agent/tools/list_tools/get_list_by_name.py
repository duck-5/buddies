import json
import logging
from typing import Any
from agent.tools.list_tools.file_based_list_tool import FileBasedListTool, FileBasedListToolConfig

logger = logging.getLogger("Tools.GetListByName")

class GetListByNameTool(FileBasedListTool):
    NAME = "get_list_by_name"
    DESCRIPTION = "Retrieves the contents of a specific list by its name."
    INPUT_FORMAT = '{"list_name": "str"}'

    def __init__(self, config: FileBasedListToolConfig) -> None:
        super().__init__(config)

    def execute(self, arguments_json: str) -> Any:
        try:
            # Parse the input arguments
            args = json.loads(arguments_json)
            list_name = args.get("list_name")

            if not list_name:
                return "Error: 'list_name' is required."

            # Load the data from the file
            data = self._load_data()

            # Retrieve the specified list
            if list_name not in data:
                return f"Error: List '{list_name}' does not exist."

            logger.info(f"Retrieved list '{list_name}'.")
            return data[list_name]

        except Exception as e:
            logger.error(f"Error in get_list_by_name: {e}")
            raise
