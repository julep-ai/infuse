# Julep
[![julep](https://socialify.git.ci/julep-ai/julep/image?description=1&descriptionEditable=Open%20platform%20for%20building%20stateful%20AI%20apps&logo=https%3A%2F%2Fraw.githubusercontent.com%2Fjulep-ai%2Fjulep%2Fdev%2F.github%2Fjulep-logo.svg&name=1&owner=1&theme=Light)](https://github.com/julep-ai/julep)  

<p align="center">
<img src="https://github.com/julep-ai/julep/blob/dev/.github/julep-meaning-banner.png?raw=true" alt="Julep: an alcoholic drink containing whisky, crushed ice, sugar, and pieces of mint" />
</p>

<p align="center">
    <a href="https://discord.gg/JzfVWsy9fY"><img src="https://img.shields.io/discord/1172458124020547584?style=social&amp;logo=discord&amp;label=discord" alt="Discord"></a>
    <span>&nbsp;</span>
    <a href="https://twitter.com/julep_ai"><img src="https://img.shields.io/twitter/follow/julep_ai?style=social&amp;logo=x" alt="X (formerly Twitter) Follow"></a>
    <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
    <a href="https://www.npmjs.com/package/@julep/sdk"><img src="https://img.shields.io/npm/v/%40julep%2Fsdk?style=social&amp;logo=npm&amp;link=https%3A%2F%2Fwww.npmjs.com%2Fpackage%2F%40julep%2Fsdk" alt="NPM Version"></a>
    <span>&nbsp;</span>
    <a href="https://pypi.org/project/julep"><img src="https://img.shields.io/pypi/v/julep?style=social&amp;logo=python&amp;label=PyPI&amp;link=https%3A%2F%2Fpypi.org%2Fproject%2Fjulep" alt="PyPI - Version"></a>
    <span>&nbsp;</span>
    <a href="https://hub.docker.com/u/julepai"><img src="https://img.shields.io/docker/v/julepai/agents-api?sort=semver&amp;style=social&amp;logo=docker&amp;link=https%3A%2F%2Fhub.docker.com%2Fu%2Fjulepai" alt="Docker Image Version"></a>
    <span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
    <a href="https://choosealicense.com/licenses/apache/"><img src="https://img.shields.io/github/license/julep-ai/julep" alt="GitHub License"></a>
</p>

---

[Julep](https://julep.ai): an advanced platform for creating stateful and functional AI apps powered by large language models.

---

## Getting Started
### Option 1: Install and run Julep locally
- Download the `docker-compose.yml` file along with the `.env` file for configuration to run the Julep platform locally

```bash
# Add the docker compose to your project dir
wget https://raw.githubusercontent.com/julep-ai/julep/dev/deploy/docker-compose.yml

# Add the .env file to your project dir
wget https://raw.githubusercontent.com/julep-ai/julep/dev/deploy/.env.example -O .env

# Pull the latest images
docker compose pull

# Start the services (in detached mode)
docker compose up -d

```
- The API would now be available at: `http://0.0.0.0:8080`

- Next, add your OpenAI API Key to the `.env`

- Set your environment variables
```bash
export JULEP_API_KEY=myauthkey
export JULEP_API_URL=http://0.0.0.0:8080
```
### Option 2: Use the Julep Cloud
- Generate an API key from https://platform.julep.ai
- Set your environment variables

```bash
export JULEP_API_KEY=your_julep_api_key
export JULEP_API_URL=https://api-alpha.julep.ai
```


### Installation

```
pip install julep
```
### Setting up the `client`

```py
from julep import Client
from pprint import pprint
import textwrap
import os

base_url = os.environ.get("JULEP_API_URL")
api_key = os.environ.get("JULEP_API_KEY")

client = Client(api_key=api_key, base_url=base_url)
```

### Create an agent
Agent is the object to which LLM settings like model, temperature along with tools are scoped to.
```py
name = "Jessica"
about = "Jessica is a stuck up Cali teenager. Showing rebellion is an evolutionary necessity for her."
default_settings = {
    "temperature": 0.7,
    "top_p": 1,
    "min_p": 0.01,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "length_penalty": 1.0,
    "max_tokens": 150,
}

agent = client.agents.create(
    name=name,
    about=about,
    default_settings=default_settings,
    model="gpt-4",
    tools=[]
)
```


### Create a user
User is the object which represents the user of the application.

Memories are formed and saved for each user and many users can talk to one agent.

```py
about = """Average nerdy techbro/girl who spends 8 hours a day in front of a laptop.
Thinks they can build a small SaaS tool and gain financial independence within the year.
"""
user = client.users.create(
    name="Anon",
    about=about,
)
```

### Create a session
A "user" and an "agent" communicate in a "session". System prompt goes here.
Conversation history and summary are stored in a "session" which saves the conversation history.

The session paradigm allows for; many users to interact with one agent and allow separation of conversation history and memories.

```py
situation_prompt = """You are Jessica. You're a stuck up Cali teenager. 
You basically complain about everything. You live in Bel-Air, Los Angeles and drag yourself to Curtis High School when you must.
"""

session = client.sessions.create(
    user_id=user.id, agent_id=agent.id, situation=situation_prompt
)
session = client.sessions.create(
    user_id=user.id, agent_id=agent.id, situation=situation_prompt
)

```

### Start a stateful conversation
`session.chat` controls the communication between the "agent" and the "user".

It has two important arguments;
- `recall`: Retrieves the previous conversations and memories.
- `remember`: Saves the current conversation turn into the memory store.

To keep the session stateful, both need to be `True`

```py
user_msg = "hey. what do u think of starbucks"
response = client.sessions.chat(
    session_id=session.id,
    messages=[
        {
            "role": "user",
            "content": user_msg,
            "name": "Anon",
        }
    ],
    recall=True,
    remember=True,
)

print("\n".join(textwrap.wrap(response.response[0][0].content, width=100)))
```

---

## Key Features
Julep offers a separation of concerns. Easing the burden and time taken to get up and running with any AI app, be it conversational, functional or agentic.


- **Statefulness By Design**:
- **Automatic Function Calling**:
- ***Work and switch between any LLMs anytime**


![alt text](image.png)

1. Stateful AI Agents: AI agents that can break down requests into multiple steps, use different tools, and maintaining state throughout the process.

2. Tools and Capabilities: Access to built-in tools (and via integrations) to perform actions including function-calling, API calls, and RAG.

3. Memory System: A sophisticated memory system that enables agents to store and recall information automatically.

4. Sessions and Tasks: Julep AI supports two main interaction modes: sessions and tasks. Sessions are short-lived, direct interactions with an agent, similar to chat. Tasks are multi-step, long-running processes designed to accomplish complex goals.

---
## What can you build with Julep?

- Cookbook Example 1
- Cookbook Example 2
- Cookbook Example 3
---

## API and SDKs
To use the API directly or to take a look at request & response formats, authentication, available endpoints and more, please refer to the [API Documentation](https://docs.julep.ai/api-reference/agents-api/agents-api)

You can also use the [Postman Collection](https://god.gw.postman.com/run-collection/33213061-a0a1e3a9-9681-44ae-a5c2-703912b32336?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D33213061-a0a1e3a9-9681-44ae-a5c2-703912b32336%26entityType%3Dcollection%26workspaceId%3D183380b4-f2ac-44ef-b018-1f65dfc8256b) for reference.

### Python SDK

To install the Python SDK, run:

```bash
pip install julep
```
For more information on using the Python SDK, please refer to the [Python SDK documentation](https://docs.julep.ai/api-reference/python-sdk-docs).


### TypeScript SDK
To install the TypeScript SDK using `npm`, run:

```bash
npm install @julep/sdk
```

For more information on using the TypeScript SDK, please refer to the [TypeScript SDK documentation](https://docs.julep.ai/api-reference/js-sdk-docs).

---

## Deployment
If you want to deploy Julep to production, [let's hop on a call](https://calendly.com/diwank-julep/45min)!

We'll help you customise the platform and help you get set up with:
- Multi-tenancy
- Reverse proxy along with authentication and authorisation
- Self-hosted LLMs
- & more

