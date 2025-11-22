from typing import Optional
from agent.tools.list_tools.list_add_item_tool import ListAddTool
from agent.tools.list_tools.list_remove_item_tool import ListRemoveTool
from agent.agent.tools.event_tools.add_event_tool import AddEventTool

AVAILABLE_TOOLS = [ListAddTool, ListRemoveTool, AddEventTool]

SHARED = "shared"

# Helper function to merge shared fields into subcategories
def do_shit(config: dict, sub_config: Optional[dict] = None, shared: dict = {}):
    if sub_config is None:
        sub_config = {}

    if isinstance(sub_config, dict):
        shared = config.get(SHARED, {})
        for key, value in config.items():
            if key != SHARED and isinstance(value, dict):
                do_shit(config, sub_config=value, shared=shared)
                
                
                


def merge_shared_fields(config):
    if isinstance(config, dict):
        shared = config.get(SHARED, {})
        for key, value in config.items():
            if key != SHARED and  isinstance(value, dict):
                # Merge shared fields recursively
                config[key] = {**shared, **merge_shared_fields(value)}
    print("=======\n", config)
    return config


TOOLS_CONFIG = merge_shared_fields({
    "ListTools": {
        SHARED: {
            "list_file_path": "lists_data.json",
        },
        ListAddTool.NAME: {
            "default_list_name": "inbox",
            "max_list_size": 5,
        },
        ListRemoveTool.NAME: {
            "allow_audit_logging": True,
        },
    },
    "EventTools": {
        SHARED: {
            "events_file_path": "events.json",
        },
        "EventCreationTools": {
            "CreateEventStrong": {
                "notification": True,
                "importance": 5,
            }
            
        }
    }  
})

