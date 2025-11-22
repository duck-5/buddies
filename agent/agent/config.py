from dataclasses import dataclass
from typing import Dict, List, Any
import toml
from datetime import datetime

# Profile:
USER_NAME = "Idit"
USER_AGE = 30
USER_CITY = "Shoham"

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

CURRENT_DATETIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
SYSTEM_PROMPT_PREFIX = f"""You are an AI agent made for helping adults.
Your user name is {USER_NAME}, age is {USER_AGE}, and lives in {USER_CITY}.
The current date and time is {CURRENT_DATETIME}.
Use friendly, caring language and keep it concise (one or two sentences).
You are capable of using tools.
After using a tool, you will receive a results summery. Your response doesn't appear the user unless all tool usage was completed.
The tool usage result summery has a status. If the status is 'success', all is well. If not, check what the issue is. You can try and recall the tool.
Use the tools to comply with the user's requests.
Remember to always respond in the requested format. All responses that aren't in the format are not helpful.
If you are requested to alert for an event, include that in the conversation. Never ignore it!
"""
RESPONSE_FORMAT = """RESPONSE FORMAT:
1. Your response must always be in raw JSON format {{ and ending with }}. Never reply in any other format.
2. The response must have the following structure:
{{
  "thought": "Your reasoning process here",
  "response": "Text response to the user (optional if using tools)",
  "end": if this field is present with value 1, the conversation will be ended.
  "tool_calls": [
    {{
      "tool_name": "name_of_tool",
      "arguments": {{ ... fields specific to the tool ... }}
    }}
  ]
}}
"""



TOOLS_DESCRIPTION = """AVAILABLE TOOLS:
{tool_descriptions}
"""
    
@dataclass
class ResponseTemplate:
  thought: str
  response: str
  tool_calls: List[ToolCall]
  
  system_prompt_template: str = SYSTEM_PROMPT_PREFIX + RESPONSE_FORMAT + TOOLS_DESCRIPTION

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

GOOGLE_API_KEY = load_google_api_key()
RESOURCES_PATH = "/home/user/buddies/resources/"
ONNX_PATH = f"{RESOURCES_PATH}/en_US-lessac-medium.onnx"
HEY_BUDDY_VOSK_MODEL_PATH = f"{RESOURCES_PATH}/model"
MAIN_STT_VOSK_MODEL_PATH = f"{RESOURCES_PATH}/vosk-model-en-us-0.42-gigaspeech"