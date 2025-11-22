from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


class Tool(ABC):
    """
    Abstract Base Class that all dynamic plugins must implement.
    """
    NAME: str
    INPUT_FORMAT: str
    DESCRIPTION: str
       
    def __init__(self, config) -> None:
        self.config = config
    
    @abstractmethod
    def execute(self, arguments_json: str) -> Any:
        """
        Executes the tool logic.
        
        Args:
            arguments_json: A JSON string containing the arguments.
            
        Returns:
            The result of the tool execution (Any serializable type).
        """
        pass