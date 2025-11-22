import json
import os
from datetime import datetime
from dataclasses import asdict

from agent.agent.flow import AgentFlow
from agent.config import EVENTS_FILE_PATH
from agent.tools.event_tools.models import Event

def check_and_alert_events(agent_flow: AgentFlow):
    """Goes over all events in EVENTS_FILE_PATH and alerts if an event needs to be notified."""
    if not os.path.exists(EVENTS_FILE_PATH):
        print("No events file found.")
        return

    with open(EVENTS_FILE_PATH, "r") as f:
        try:
            events = json.load(f)
            events = [Event(**event) for event in events]
        except json.JSONDecodeError:
            print("Failed to parse events file.")
            return

    current_time = datetime.now()

    for event in events:
        event_time = datetime.fromisoformat(event.time)
        notification = event.notification
        description = event.description

        # Check if the event needs to be alerted
        if notification and current_time >= event_time and not event.has_passed:
            print(f"ALERT: Event '{description}' is happening now or has passed!")
            agent_flow.add_note(f"ALERT: Event '{description}' at time {event.time} is happening now or has passed!")
            ... # Additional alert handling logic can be added here
        
            event.has_passed = True
    # Save updated events back to file
    with open(EVENTS_FILE_PATH, "w") as f:
        json.dump([asdict(event) for event in events], f, indent=2)


def pool_events_handler(agent_flow: AgentFlow):
    """Periodically checks for events to alert."""
    import time
    while True:
        check_and_alert_events(agent_flow)
        time.sleep(5)