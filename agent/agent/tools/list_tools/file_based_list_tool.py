import json
import os
import logging
from typing import Dict, List
from agent.tools.tool_interface import Tool

logger = logging.getLogger("Tools.Lists")

class FileBasedListTool(Tool):
    """Base class for list tools dealing with file I/O."""
    
    def _get_file_path(self) -> str:
        return self.config["list_file_path"]

    def _load_data(self) -> Dict[str, List[str]]:
        path = self._get_file_path()
        if not os.path.exists(path):
            return {}
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load list data from {path}: {e}")
            return {}

    def _save_data(self, data: Dict[str, List[str]]) -> None:
        path = self._get_file_path()
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save list data to {path}: {e}")
            raise
