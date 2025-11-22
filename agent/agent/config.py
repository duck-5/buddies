from dataclasses import dataclass
from typing import Dict, List, Any
import toml

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
Note that sometimes the tools won't work. You must validate the tool_results section in responses and make sure that the statues is success.
If not, understand the error and recall the tool.
RESPONSE FORMAT:
1. Your response must always be in raw JSON format {{ and ending with }}. Never reply in any other format.
2. The response must have the following structure:
{{
  "thought": "Your reasoning process here",
  "response": "Text response to the user (optional if using tools)",
  "tool_calls": [
    {{
      "tool_name": "name_of_tool",
      "arguments": {{ ... fields specific to the tool ... }}
    }}
  ]
}}

AVAILABLE TOOLS:
{tool_descriptions}"""

EVENTS_FILE_PATH = "events.json"
LISTS_FILE_PATH = "lists.json"

def load_google_api_key(secrets_file: str = "secrets.toml") -> str:
    """Load the Google API key from the secrets.toml file."""
    try:
        with open(secrets_file, "r") as file:
            secrets = toml.load(file)
            return secrets.get("GOOGLE_API_KEY", "")
    except FileNotFoundError:
        raise FileNotFoundError(f"Secrets file '{secrets_file}' not found.")
    except Exception as e:
        raise RuntimeError(f"Failed to load Google API key: {e}")

# Example usage
GOOGLE_API_KEY = load_google_api_key()