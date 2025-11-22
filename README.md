# AI Buddies - Agent System

## Overview
AI Buddies is a modular and extensible agent system designed to handle various tasks using tools. The system is built with a focus on flexibility, allowing developers to add, configure, and manage tools easily. The agent system processes user inputs, executes tools, and provides meaningful responses.

## Components

### 1. **Agent System**
The core of the application, responsible for:
- Loading configurations.
- Managing tools.
- Parsing and executing user inputs.

#### Key Files:
- `agent_system.py`: Implements the main logic for managing tools and processing user inputs.
- `agent_config.py`: Contains configuration settings for the agent, including tool configurations and logging settings.

### 2. **Tools**
Tools are modular components that perform specific tasks. Each tool implements a common interface and can be dynamically added to the system.

#### Tool Categories:
- **Event Tools**: Manage events, including creation and removal.
  - `add_event_tool.py`: Allows users to create events with fields like time, notification, importance, and description.
  - `remove_event_tool.py`: Enables users to remove events based on a unique identifier or description.
- **List Tools**: Handle operations on lists, such as adding or removing items.
  - `file_based_list_tool.py`: A base class for tools that interact with file-based lists.

#### Tool Interface:
- `tool_interface.py`: Defines the `Tool` abstract base class that all tools must implement. This ensures consistency and standardization across tools.

### 3. **Plugins**
Plugins extend the functionality of the agent system by providing additional tools. The `AVAILABLE_TOOLS` list in the `plugins` module dynamically loads all registered tools.

#### Key Files:
- `__init__.py`: Registers tools and makes them available to the agent system.

### 4. **Event Management**
The system includes robust event management capabilities:
- Events are stored in a JSON file (`events.json`).
- Tools like `AddEventTool` and `RemoveEventTool` interact with this file to manage events.
- The `events_handler.py` script processes events and alerts users when necessary.

### 5. **Configuration**
The agent system uses a Python-based configuration file (`agent_config.py`) to manage settings. This includes:
- Tool-specific configurations.
- Logging settings.
- Error messages.

### 6. **Logging**
The system includes a flexible logging mechanism to track operations and errors. Logging settings can be customized in `agent_config.py`.

## Recent Updates

### 1. **Speech-to-Text and Text-to-Speech Integration**
- Added `SpeechToText` for capturing user input via voice commands.
- Integrated `tts.talk` for generating audio responses to the user.
- Configured the VOSK model path for speech recognition.

### 2. **Enhanced Agent Flow**
- The `AgentFlow` class now supports:
  - Listening to user input via `SpeechToText`.
  - Generating audio responses using `TextToSpeech`.
  - Handling tool usage reports and ensuring proper execution.
- Improved error handling during LLM response processing.

### 3. **System Prompt Updates**
- The system prompt now includes user-specific details (name, age, city) and the current date/time.
- Example: "The current date and time is 2025-11-22 14:30:00."

### 4. **New Tools and Features**
- **GetEventsTool**: Retrieve events by date range, supporting ISO 8601 datetime format.
- **GetListByNameTool**: Retrieve the contents of a specific list by its name.
- **GetListsHeadersTool**: Retrieve the headers of all lists in the system.

### 5. **Google API Key Integration**
- The system securely loads the Google API key from a `secrets.toml` file.

### 6. **Manual Testing Support**
- Added a manual test for the `GetEventsTool` to validate its functionality. The test can be run independently, and the output is printed for review.

## Future Plans
- Add more tools for advanced list and event management.
- Implement automated tests for all tools.
- Enhance the logging system to include more granular details.
- Expand speech recognition capabilities to support multiple languages.

## How to Use

### 1. **Setup**
1. Clone the repository.
2. Install dependencies.
3. Configure the `agent_config.py` file as needed.

### 2. **Run the Agent**
Execute the `main.py` script to start the agent system.

```bash
python main.py
```

### 3. **Add and Remove Events**
- Use the `AddEventTool` to create events.
- Use the `RemoveEventTool` to delete events.

### 4. **Event Alerts**
Run the `events_handler.py` script to check for and alert upcoming events.

```bash
python buddy/events_handler.py
```

## Extending the System
To add a new tool:
1. Implement the `Tool` interface in `tool_interface.py`.
2. Add the tool to the `AVAILABLE_TOOLS` list in `plugins/__init__.py`.
3. Configure the tool in `agent_config.py` if needed.

## License
This project is licensed under the MIT License.