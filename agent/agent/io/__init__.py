"""IO subpackage for LLM communication.

This package provides interfaces and implementations for communicating
with external LLM services.
"""

from agent.io.llm_client import LLMClient
from agent.io.mock_llm_client import MockLLMClient

__all__ = ["LLMClient", "MockLLMClient"]

