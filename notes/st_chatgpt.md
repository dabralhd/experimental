## 20-2-2025
- support for Agents and Reasoning models ongoing
- OpenaI O3 reasoning model coming in Q3
- enahnce RAG capabilities
### Reasoning models
- are able to think multiple approaches and then suggest best ones
- cons: more expensive, long time to reply, Pros: 
- Candidates: Open AI o1, o3 | Grok v3 (twitter) | Deepseek R1

Reasoning models are slower because:
- we can give model time to think say 10s, 20s
- typically user can see what model is thinking

OpenAI roadmap:
- available now: GPT 4o, o1 and o3
- GPT 4.5 in weeks (last classical model)
- GPT 5 universal model
    - in this year, may be june, july

### Agents
- agents can use tools 
- RAG
Agents can use other agents, agent crews
each sub agent has its own tools
e.g. an orchestrator agent can use crew of [quality agent, sales agent, planning agent]
Agent actions can be subject to human approvals

ST ChatGPT 2.3 features
- New API
    - upload docs using scripts
    - 
- Smart Agent
- You cannot create your persona, or knowledge base
- cannot create one from scratch

New set of API
- all knowledge base features of chatgpt
  - kb-query: implement semantic search, recommendation system, anomaly detection
  - kb-datasource-info
  - kb-datasource-new: ceate new datasource

  ST ChatGPT architecture is flexible, and can use different models from different vendors.