from dataclasses import dataclass
import json
import logging
from typing import Any
from agent.tools.list_tools.models import ListItem
from agent.tools.list_tools.file_based_list_tool import FileBasedListTool, FileBasedListToolConfig
logger = logging.getLogger("Tools.ListRemoveItem")

@dataclass
class ListRemoveToolConfig(FileBasedListToolConfig):
    allow_audit_logging: bool

class ListRemoveTool(FileBasedListTool):
    NAME="remove_from_list"
    DESCRIPTION="Removes an item from a list."
    INPUT_FORMAT='{"item": "str", "list_name": "str"}'

    def __init__(self, config: ListRemoveToolConfig) -> None:
        super().__init__(config)
    
    def execute(self, arguments_json: str) -> Any:
        try:
            args = json.loads(arguments_json)
            item = ListItem(**args)
            
            audit = self.config.allow_audit_logging

            data = self._load_data()

            if item.list_name not in data:
                return f"Error: List '{item.list_name}' does not exist."

            if item.item in data[item.list_name]:
                data[item.list_name].remove(item.item)
                self._save_data(data)
                
                if audit:
                    logger.info(f"[AUDIT] Removed '{item}' from '{item.list_name}'")
                return f"Success: Removed '{item.item}'."
            
            return f"Error: Item '{item.item}' not found."

        except Exception as e:
            logger.error(f"Error in remove_from_list: {e}")
            raise

