"""Google Gemini implementation of LLMClient.

This module provides a client for communicating with Google's Gemini API.
"""

import logging
from typing import Any, Dict, Optional

import google.generativeai as genai

from agent.llm.llm_client import LLMClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("IO.GeminiClient")

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class GeminiConfig:
    """Configuration for the Gemini Client."""
    api_key: str
    model_name: str = "models/gemini-2.5-flash"
    chat_mode: bool = False
    temperature: float = 0.7
    max_output_tokens: Optional[int] = None


class GeminiClient(LLMClient):
    """
    Google Gemini implementation of LLMClient using a Dataclass configuration.
    """

    def __init__(self, config: GeminiConfig) -> None:
        """
        Initialize the Gemini client.

        Args:
            config: A GeminiConfig object containing api_key, model_name, etc.
        """
        # We store the specific config object
        self.config = config
        self.chat_session = None

        # Validate critical fields
        if not self.config.api_key:
            raise ValueError("GeminiConfig.api_key is required.")

        # Configure the global genai library
        # Note: In a multi-client setup, you might need to handle this differently
        genai.configure(api_key=self.config.api_key)

        logger.info(
            f"Initialized GeminiClient with model: {self.config.model_name}, "
            f"Chat Mode: {self.config.chat_mode}"
        )

    def call(self, system_prompt: str, user_message: str) -> str:
        """
        Send a request to Gemini.
        """
        try:
            # --- CHAT MODE (Stateful) ---
            if self.config.chat_mode:
                if self.chat_session is None:
                    logger.debug("Starting new chat session with system prompt.")
                    model = self._create_model(system_prompt)
                    self.chat_session = model.start_chat(history=[])
                
                response = self.chat_session.send_message(user_message)

            # --- STANDARD MODE (Stateless) ---
            else:
                # Create a fresh model for every call
                model = self._create_model(system_prompt)
                response = model.generate_content(user_message)

            if not response.text:
                raise RuntimeError("No response text received from Gemini.")

            return response.text

        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            raise

    def _create_model(self, system_instruction: str) -> genai.GenerativeModel:
        """Helper to create the model object based on current config."""
        generation_config = genai.types.GenerationConfig(
            temperature=self.config.temperature,
            max_output_tokens=self.config.max_output_tokens
        )
        
        return genai.GenerativeModel(
            model_name=self.config.model_name,
            system_instruction=system_instruction,
            generation_config=generation_config
        )

    def update_config(self, new_config: GeminiConfig) -> None:
        """
        Replaces the current configuration with a new one.
        Resets the chat session if model or critical settings change.
        """
        # Check if we need to reset the chat session
        reset_needed = (
            new_config.model_name != self.config.model_name or
            new_config.chat_mode != self.config.chat_mode or
            new_config.system_prompt_hash != getattr(self.config, 'system_prompt_hash', None) # Advanced usage
        )
        
        # Re-authenticate if key changed
        if new_config.api_key != self.config.api_key:
             genai.configure(api_key=new_config.api_key)

        self.config = new_config
        
        if reset_needed:
            self.chat_session = None
            logger.info("Configuration updated: Chat session reset.")
        else:
            logger.info("Configuration updated.")