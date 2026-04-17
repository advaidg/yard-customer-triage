"""Auto-generated Chain Executor for Customer Triage."""
import asyncio
import httpx
from fastapi import FastAPI

app = FastAPI(title="Customer Triage")

TOKEN = ""
AGENTS = [
    {"id": "node-c79f4402", "agent_id": "0cc9608a-ca68-4b03-aa76-0c100349b42e", "endpoint": "", "timeout": 30},
    {"id": "node-96154bd7", "agent_id": "01b5576b-07d6-46f2-85c3-d66eafb4ea1b", "endpoint": "", "timeout": 30},
    {"id": "node-3f15cce0", "agent_id": "0c464689-3fc8-4142-8beb-c33a32e62a8a", "endpoint": "", "timeout": 30},
]

EDGES = [
    {"id": "", "source": "node-c79f4402", "target": "node-96154bd7", "transform": "passthrough"},
    {"id": "", "source": "node-96154bd7", "target": "node-3f15cce0", "transform": "passthrough"},
]


async def call_agent(endpoint: str, input_data: dict) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(endpoint, json={"input": input_data}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=300)
        resp.raise_for_status()
        return resp.json()


@app.post("/invoke")
async def invoke(input: dict):
    current = input.get("input", input)
    trace = []
    for agent in AGENTS:
        try:
            result = await call_agent(agent["endpoint"], current)
            trace.append({"agent": agent["id"], "status": "completed", "output": result})
            current = result.get("output", result)
        except Exception as e:
            trace.append({"agent": agent["id"], "status": "failed", "error": str(e)})
    return {"output": current, "trace": trace, "status": "completed"}


@app.get("/health")
async def health():
    return {"status": "ok", "engine": "chain_executor", "agents": len(AGENTS)}