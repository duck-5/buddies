from agent.tools.list_tools.list_add_item_tool import ListAddTool
from agent.tools.list_tools.list_remove_item_tool import ListRemoveTool

AVAILABLE_TOOLS = [ListAddTool, ListRemoveTool]

SHARED = "shared"

# Helper function to merge shared fields into subcategories
def merge_shared_fields(config):
    if isinstance(config, dict):
        shared = config.get(SHARED, {})
        for key, value in config.items():
            if key != SHARED and isinstance(value, dict):
                # Merge shared fields recursively
                config[key] = {**shared, **merge_shared_fields(value)}
    return config


TOOLS_CONFIG = merge_shared_fields({
    SHARED: {
        "list_file_path": "lists_data2.json",
    },
    ListAddTool.NAME: {
        "default_list_name": "inbox",
        "max_list_size": 5,
    },
    ListRemoveTool.NAME: {
        "allow_audit_logging": True,
    },
})

