from __future__ import annotations
from agent.tools.list_tools.list_add_item_tool import ListAddTool, ListAddToolConfig
from agent.tools.list_tools.list_remove_item_tool import ListRemoveTool, ListRemoveToolConfig
from agent.tools.event_tools.add_event_tool import AddEventTool, AddEventToolConfig
from agent.tools.event_tools.remove_event_tool import RemoveEventTool, RemoveEventToolConfig
from agent.agent_config import LISTS_FILE_PATH, EVENTS_FILE_PATH

AVAILABLE_TOOLS = [ListAddTool, ListRemoveTool, AddEventTool, RemoveEventTool]


TOOLS_CONFIG = {
    ListAddTool.NAME: ListAddToolConfig(
        list_file_path=LISTS_FILE_PATH,
        default_list_name="inbox",
        max_list_size=5
    ),
    ListRemoveTool.NAME: ListRemoveToolConfig(
        list_file_path=LISTS_FILE_PATH,
        allow_audit_logging=True
    ),

    AddEventTool.NAME: AddEventToolConfig(
        event_files_path=EVENTS_FILE_PATH
    ),
    RemoveEventTool.NAME: RemoveEventToolConfig(
        events_file_path=EVENTS_FILE_PATH
    ),
    
}   