"""Google Gemini implementation of LLMClient.

This module provides a client for communicating with Google's Gemini API.
"""

import logging
from typing import Any, Dict, Optional

import google.generativeai as genai

from agent.io.llm_client import LLMClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("IO.GeminiClient")


class GeminiClient(LLMClient):
    """
    Google Gemini implementation of LLMClient.
    
    Communicates with Google's Gemini API using the google-generativeai library.
    """
    
    DEFAULT_MODEL = "models/gemini-2.5-flash"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Gemini client.
        
        Args:
            config: Configuration dictionary. Required keys:
                   - "api_key": Google API key for authentication
                   Optional keys:
                   - "model_name": Model to use (default: "models/gemini-2.0-flash-exp")
                   Note: Tools support is currently disabled.
        
        Raises:
            ImportError: If google-generativeai is not installed.
            ValueError: If api_key is not provided in config.
        """
        super().__init__(config)

        
        api_key = self.config.get("api_key")
        if not api_key:
            raise ValueError("'api_key' is required in config for GeminiClient")
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Get model name from config
        self.model_name = self.config.get("model_name", self.DEFAULT_MODEL)        # Tools support is disabled - always use empty list
        
        logger.info(f"Initialized GeminiClient with model: {self.model_name}")
    
    def call(self, system_prompt: str, user_message: str) -> str:
        """
        Send a request to Gemini and return the response.
        
        Args:
            system_prompt: The system prompt containing instructions and
                          tool descriptions for the LLM.
            user_message: The user's message or query to process.
        
        Returns:
            The raw response from Gemini as a string. Expected to be
            valid JSON matching the agent protocol format.
        
        Raises:
            Exception: For API errors, network errors, or other failures.
        """
        try:
            # Recreate model with the system prompt (system_instruction)
            # Note: We recreate it each time in case the system prompt changes
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt)

            logger.debug(f"Sending request to Gemini (model: {self.model_name})")
            logger.debug(f"System prompt: {system_prompt}")
            logger.debug(f"User message: {user_message}")
            
            # Generate content
            response = model.generate_content(user_message)
            
            # Extract text from response
            response_text = response.text if response.text else ""
            response_text = response_text[response_text.find('{'):-response_text[::-1].find('}')+1] 

            logger.debug(f"Received response from Gemini (length: {len(response_text)} characters)")
            logger.debug(f"Full Gemini response: {response_text}")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            raise
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Update the client configuration.
        
        Note: If api_key or model_name changes, the client will need to be
        reinitialized. This method only updates the config dictionary.
        
        Args:
            config: Configuration dictionary to merge with existing config.
        """
        super().configure(config)
        
        # If api_key changed, reconfigure
        if "api_key" in config:
            genai.configure(api_key=config["api_key"])
            logger.info("Updated Gemini API key")
        
        # If model_name changed, update it
        if "model_name" in config:
            self.model_name = config["model_name"]
            logger.info(f"Updated model name to: {self.model_name}")
