from dataclasses import dataclass
from typing import Dict, List, Any

# --- AGENT CONFIGURATION ---
# --- LOGGING CONFIGURATION ---
@dataclass
class LoggingConfig:
    """Configuration for the system logging."""
    # Actual values inserted
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    datefmt: str = "%H:%M:%S"


# --- PROTOCOL CONFIGURATION ---
@dataclass
class ProtocolConfig:
    """Defines the expected keys in the Agent's structured JSON response."""
    # Actual values inserted
    key_thought: str = "thought"
    key_response: str = "response"
    key_tool_calls: str = "tool_calls"
    key_tool_name: str = "tool_name"
    key_arguments: str = "arguments"

# --- ERROR MESSAGES ---
@dataclass
class ErrorMessages:
    """Templated error messages for various failure modes."""
    # Actual values inserted
    json_parse: str = "CRITICAL: Failed to parse JSON response. Error: {error}"
    tool_not_found: str = "ERROR: Tool '{tool_name}' is not available."
    execution_error: str = "ERROR: Tool '{tool_name}' failed during execution. Details: {error}"

  
  
@dataclass
class ToolCall:
  tool_name: str
  arguments: Dict[str, Any]  
    
@dataclass
class ResponseTemplate:
  thought: str
  response: str
  tool_calls: List[ToolCall]
  
  system_prompt_template: str = """You are an AI agent capable of using tools.

RESPONSE FORMAT:
You must respond in strictly valid JSON format with the following structure:
{
  "thought": "Your reasoning process here",
  "response": "Text response to the user (optional if using tools)",
  "tool_calls": [
    {
      "tool_name": "name_of_tool",
      "arguments": { ... fields specific to the tool ... }
    }
  ]
}

AVAILABLE TOOLS:
{tool_descriptions}"""
