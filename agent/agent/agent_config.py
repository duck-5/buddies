# Configuration for the Agent System

# String constants for keys
PLUGINS_DIRECTORY = "plugins_directory"
SYSTEM_PROMPT_TEMPLATE = "system_prompt_template"
LEVEL = "level"
FORMAT = "format"
DATEFMT = "datefmt"
KEY_THOUGHT = "key_thought"
KEY_RESPONSE = "key_response"
KEY_TOOL_CALLS = "key_tool_calls"
KEY_TOOL_NAME = "key_tool_name"
KEY_ARGUMENTS = "key_arguments"
JSON_PARSE = "json_parse"
TOOL_NOT_FOUND = "tool_not_found"
EXECUTION_ERROR = "execution_error"
AGENT_CONFIG = {
    PLUGINS_DIRECTORY: "plugins",
    SYSTEM_PROMPT_TEMPLATE: """You are an AI agent capable of using tools.

RESPONSE FORMAT:
You must respond in strictly valid JSON format with the following structure:
{
  \"thought": "Your reasoning process here",
  "response": "Text response to the user (optional if using tools)",
  "tool_calls": [
    {
      "tool_name": "name_of_tool",
      "arguments": { ... fields specific to the tool ... }
    }
  ]
}

AVAILABLE TOOLS:
{tool_descriptions}""",
}

LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "datefmt": "%H:%M:%S",
}

PROTOCOL_CONFIG = {
    "key_thought": "thought",
    "key_response": "response",
    "key_tool_calls": "tool_calls",
    "key_tool_name": "tool_name",
    "key_arguments": "arguments",
}

ERROR_MESSAGES = {
    "json_parse": "CRITICAL: Failed to parse JSON response. Error: {error}",
    "tool_not_found": "ERROR: Tool '{tool_name}' is not available.",
    "execution_error": "ERROR: Tool '{tool_name}' failed during execution. Details: {error}",
}
