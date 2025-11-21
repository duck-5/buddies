from abc import ABC, abstractmethod
from typing import Any, Dict


class Tool(ABC):
    """
    Abstract Base Class that all dynamic plugins must implement.
    """
    NAME: str
    INPUT_FORMAT: str
    DESCRIPTION: str
       
    def __init__(self) -> None:
        self.config: Dict[str, Any] = {}

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Injects tool-specific configuration from the TOML file.
        """
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