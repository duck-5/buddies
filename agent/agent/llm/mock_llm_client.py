"""Mock implementation of LLMClient for testing and development.

This module provides a mock LLM client that returns predefined responses
without making actual API calls.
"""

import json
import logging
from typing import Any, Dict, Optional

from agent.llm.llm_client import LLMClient

logger = logging.getLogger("IO.MockLLMClient")


DEFAULT_MOCK_RESPONSE = """{
    "thought": "Adding milk using defaults.",
    "tool_calls": [
        {
            "tool_name": "add_to_list",
            "arguments": {
                "list_name": "groceries",
                "item": "milk"
            }
        }
    ]
}"""

class MockLLMClient(LLMClient):
    """
    Mock implementation of LLMClient that returns hardcoded responses.
    
    Useful for testing and development without making actual API calls.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the mock LLM client.
        
        Args:
            config: Optional configuration dictionary. Can include:
                   - "response": Custom JSON response string to return
                   - "responses": List of responses to cycle through
        """
        super().__init__(config)
        self._response_index = 0
    
    def call(self, system_prompt: str, user_message: str) -> str:
        """
        Return a mock JSON response without making an API call.
        
        Args:
            system_prompt: The system prompt (ignored in mock).
            user_message: The user message (ignored in mock).
        
        Returns:
            A JSON string matching the agent protocol format.
        """
        # Check if a custom response is configured
        if "response" in self.config:
            logger.debug("Using configured mock response")
            return self.config["response"]
        
        # Check if multiple responses are configured (for testing different scenarios)
        if "responses" in self.config:
            responses = self.config["responses"]
            if isinstance(responses, list) and len(responses) > 0:
                response = responses[self._response_index % len(responses)]
                self._response_index += 1
                logger.debug(f"Using response {self._response_index - 1} from configured responses")
                return response
        
        # Default mock response
        default_response = {
            "thought": "Adding milk using defaults.",
            "tool_calls": [
                {
                    "tool_name": "add_to_list",
                    "arguments": {
                        "list_name": "groceries",
                        "item": "milk"
                    }
                }
            ]
        }
        
        logger.debug("Using default mock response")
        return json.dumps(default_response, indent=2)

