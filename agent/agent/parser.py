import json
from dataclasses import asdict
import logging
from typing import Any, Dict, List
from agent.utils import utils
from agent.tools.tool_interface import Tool
from agent.tools import AVAILABLE_TOOLS, TOOLS_CONFIG
from agent.agent.config import LoggingConfig, ErrorMessages, ResponseTemplate

# Configure Logging
logging.basicConfig(
    level=LoggingConfig.level,
    format=LoggingConfig.format,
    datefmt=LoggingConfig.datefmt
)
logger = logging.getLogger("AgentSystem")


class Config:
    def __init__(self):
        self._tools_config = TOOLS_CONFIG
        self._error_messages = ErrorMessages()
        self._response_template = ResponseTemplate

    @property
    def prompt_template(self) -> str:
        return self._response_template.system_prompt_template

    @property
    def tools_config(self) -> Dict[str, Any]:
        return self._tools_config

    @property
    def error_messages(self) -> Dict[str, str]:
        return asdict(self._error_messages)

    def get_error(self, key: str, **kwargs) -> str:
        msg = self.error_messages.get(key, "Unknown Error")
        return msg.format(**kwargs)


# --- The Parser ---

class AgentParser:
    def __init__(self, config: Config):
        self.config = config
        self.tools: Dict[str, Tool] = self._get_tools(config)
        self.tool_descriptions = self._build_descriptions()

    @staticmethod
    def _get_tools(config):
        return {tool.NAME: tool(config.tools_config.get(tool.NAME, {})) for tool in AVAILABLE_TOOLS}
        
    
    def _build_descriptions(self) -> str:
        descs = []
        for tool in self.tools.values():
            descs.append(
                f"- Name: {tool.NAME}\n"
                f"  Desc: {tool.DESCRIPTION}\n"
                f"  Args: {tool.INPUT_FORMAT}"
            )
        return "\n".join(descs)

    def get_system_prompt(self) -> str:
        return self.config.prompt_template.format(
            tool_descriptions=self.tool_descriptions
        )

    def parse_and_execute(self, llm_response: str) -> List[Dict[str, Any]]:

        try:
            data = utils.parse_llm_response(llm_response)
        except ValueError:
            logger.error("Could not parse LLM response")
            logger.debug(f"Full response: {llm_response}")
            return []

        results = []
        if "thought" in data:
            logger.info(f"[AI Thought]: {data['thought']}")
        if "response" in data:
            logger.info(f"[AI Message]: {data['response']}")

        tool_calls = data.get("tool_calls", [])
        for call in tool_calls:
            tool_name = call.get("tool_name")
            args_dict = call.get("arguments", {})
            args_str = json.dumps(args_dict)
            if tool_name in self.tools:
                logger.info(f"Invoking tool: {tool_name}")
                try:
                    output = self.tools[tool_name].execute(args_str)
                    results.append({"tool": tool_name, "status": "success", "output": output})
                    logger.info(f"Tool '{tool_name}' execution successful.")
                except Exception as e:
                    err_msg = self.config.get_error("execution_error", tool_name=tool_name, error=str(e))
                    results.append({"tool": tool_name, "status": "error", "output": err_msg})
                    logger.error(f"Tool execution failed: {err_msg}")
            else:
                err_msg = self.config.get_error("tool_not_found", tool_name=tool_name)
                results.append({"tool": tool_name, "status": "error", "output": err_msg})
                logger.error(err_msg)

        return results
