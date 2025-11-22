"""Abstract interface for LLM clients.

This module defines the abstract base class that all LLM client
implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class LLMClient(ABC):
    """
    Abstract base class for LLM client implementations.
    
    All LLM clients must implement this interface to ensure consistent
    interaction with the agent system.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the LLM client.
        
        Args:
            config: Optional configuration dictionary for the client.
                   Implementation-specific settings can be passed here.
        """
        self.config: Dict[str, Any] = config or {}
    
    @abstractmethod
    def call(self, system_prompt: str, user_message: str) -> str:
        """
        Send a request to the LLM and return the response.
        
        This method should send the system prompt and user message to the
        LLM service and return the raw response as a string. The response
        is expected to be in JSON format as defined by the agent protocol.
        
        Args:
            system_prompt: The system prompt containing instructions and
                          tool descriptions for the LLM.
            user_message: The user's message or query to process.
        
        Returns:
            The raw response from the LLM as a string. Expected to be
            valid JSON matching the agent protocol format.
        
        Raises:
            Implementation-specific exceptions for network errors,
            API errors, or other failures.
        """
        pass
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Update the client configuration.
        
        Args:
            config: Configuration dictionary to merge with existing config.
        """
        self.config.update(config)

