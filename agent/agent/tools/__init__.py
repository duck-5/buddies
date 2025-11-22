from __future__ import annotations
from agent.tools.list_tools.file_based_list_tool import FileBasedListToolConfig
from agent.tools.list_tools.list_add_item_tool import ListAddTool, ListAddToolConfig
from agent.tools.list_tools.list_remove_item_tool import ListRemoveTool, ListRemoveToolConfig
from agent.tools.event_tools.add_event_tool import AddEventTool, AddEventToolConfig
from agent.tools.event_tools.remove_event_tool import RemoveEventTool, RemoveEventToolConfig
from agent.tools.event_tools.get_events_tool import GetEventsTool, GetEventsToolConfig
from agent.tools.list_tools.get_lists_headers import GetListsHeadersTool
from agent.tools.list_tools.get_list_by_name import GetListByNameTool

from agent.config import LISTS_FILE_PATH, EVENTS_FILE_PATH

AVAILABLE_TOOLS = [ListAddTool, ListRemoveTool, AddEventTool, RemoveEventTool, GetEventsTool, GetListsHeadersTool, GetListByNameTool]


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
    GetListByNameTool.NAME: FileBasedListToolConfig(
        list_file_path=LISTS_FILE_PATH
    ),
    GetListsHeadersTool.NAME: FileBasedListToolConfig(
        list_file_path=LISTS_FILE_PATH
    ),
    
    AddEventTool.NAME: AddEventToolConfig(
        event_files_path=EVENTS_FILE_PATH
    ),
    RemoveEventTool.NAME: RemoveEventToolConfig(
        events_file_path=EVENTS_FILE_PATH
    ),
    GetEventsTool.NAME: GetEventsToolConfig(
        events_file_path=EVENTS_FILE_PATH
    ),
    
}   