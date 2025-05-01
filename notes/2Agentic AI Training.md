# Agentic AI training

1. Intro
Autogen: open source programming fw
- toolkit to build and manage AI agents
- code first

Autogen Studio (AGS): 
- part of autogen, visual tool
- does not provide all features of AutoGen

what can be done with AGS:
- define agents workflows, 
- simulations

API key: https://platform.openai.com/api-keys

2. setting up autogen studio:
- install conda, python 3.10
- launch conda prompt
```
conda create -n ags6 python=3.11
conda activate ags6
pip install autogenstudio
autogenstudio ui --port 8081
```
- got to localhost:8081
- goto models and clone gpt-4o
- paste api key

 2.1 Explore AGS
- two main sections: Build, Playground

3. Components of AI Agent
skills, LLM, Agents/persona
ConversableAgent --> AssistantAgent, UserProxyAgent, GroupChatManager (coordination task, manage multiple agent)

how to create an Agent:
1. Define a skill
2. Configure a model
3. build the agent
4. add it to a workflow
once done, Test in playground


Designing Agentic workflow
two architecture: autonomous chat, sequenctial chat

Creating an agentic workflow: UserProxyAgent (proxy for receiving inputs from user), AssistantAgent (powered by LLM, returns structured reqplies, uses skills)

