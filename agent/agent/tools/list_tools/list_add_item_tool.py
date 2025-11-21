import json
import os
import logging
from typing import Any, Dict, List

from agent.tools.list_tools.file_based_list_tool import FileBasedListTool

logger = logging.getLogger("Tools.ListAddItem")

class ListAddTool(FileBasedListTool):
    NAME = "add_to_list"
    DESCRIPTION = "Adds a specific item to a named list."
    INPUT_FORMAT = '{"item": "str", "list_name": "str (optional)"}'

    def execute(self, arguments_json: str) -> Any:
        try:
            args = json.loads(arguments_json)
            
            # Config
            default_list = self.config.get("default_list_name", "inbox")
            max_size = self.config.get("max_list_size", 100)
            
            item = args.get("item")
            list_name = args.get("list_name", default_list)
            
            if not item:
                return "Error: 'item' is required."

            data = self._load_data()
            
            if list_name not in data:
                data[list_name] = []
                logger.info(f"Created new list '{list_name}' in {self._get_file_path()}")

            current_list = data[list_name]
            
            if len(current_list) >= max_size:
                logger.warning(f"List '{list_name}' limit reached.")
                return f"Error: List '{list_name}' is full."

            current_list.append(item)
            self._save_data(data)
            
            logger.info(f"Persisted '{item}' to list '{list_name}'")
            return f"Success: Added '{item}' to '{list_name}'."

        except Exception as e:
            logger.error(f"Error in add_to_list: {e}")
            raise
