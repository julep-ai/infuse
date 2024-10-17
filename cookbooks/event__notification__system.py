# -*- coding: utf-8 -*-
"""Event _Notification_ System.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YWmfcFC_iAGCC8McnGowynjS77HtLpyf
"""

import uuid
import yaml
import time
from julep import Client

# Generate unique UUIDs
AGENT_UUID = uuid.uuid4()
EVENT_NOTIFICATION_TASK_UUID = uuid.uuid4()

api_key = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM4NTQzOTUsImlhdCI6MTcyODY3MDM5NSwic3ViIjoiYmIzZjZlMDYtYWE5Yi01OWRkLWJkZmQtOGRmMzk4Y2ZiZjY4In0.SAA0Vi4X68DclecawNvLAihdcsLUaT36oKdGIRunr8AtQPMxWgHSLCub_rPwMmOpV3D0muq5Z--Lw-_br5sqIQ" # Add your Julep API key
client = Client(api_key=api_key, environment="dev")

# Create or update the notification agent
agent = client.agents.create_or_update(
    agent_id=AGENT_UUID,
    name="Event-Driven Notification Agent",
    about="Agent for sending notifications based on specific event triggers.",
    model="gpt-4o",
)

# Define the event notification task with corrected evaluate step
event_notification_task_def = yaml.safe_load("""
name: Event Notification

input_schema:
  type: object
  properties:
    event_type:
      type: string
    event_detail:
      type: object
      properties:
        description:
          type: string
        trigger_time:
          type: string

main:
- prompt:
  - role: system
    content: >-
      You are managing an event-driven notification system. The event is:
      Type: {{inputs[0].event_type}}
      Detail: {{inputs[0].event_detail.description}}
      Trigger Time: {{inputs[0].event_detail.trigger_time}}

      Notify the user if this event needs attention.
  unwrap: true

- evaluate:
    expression: "'Notify User: ' + str(True)"  # Return a valid string

- return:
    notify_user: "{{ _.expression }}"
""")

# Create or update the event task
event_notification_task = client.tasks.create_or_update(
    task_id=EVENT_NOTIFICATION_TASK_UUID,
    agent_id=AGENT_UUID,
    **event_notification_task_def
)

# Function to trigger notifications based on events
def trigger_event_notification(event_type, description, trigger_time):
    execution = client.executions.create(
        task_id=EVENT_NOTIFICATION_TASK_UUID,
        input={
            "event_type": event_type,
            "event_detail": {
                "description": description,
                "trigger_time": trigger_time
            }
        }
    )
    time.sleep(2)
    result = client.executions.get(execution.id)
    return client.executions.transitions.list(execution_id=result.id).items[0].output

# Example usage of event-driven notification system
print("Event-Driven Notification System:")

event_type = "Stock Price Change"
description = "AAPL stock price exceeded $150"
trigger_time = "2024-10-17T15:00:00Z"

notification = trigger_event_notification(event_type, description, trigger_time)
if notification:
    print(f"Notification: Event '{event_type}' triggered at {trigger_time} - {description}")

