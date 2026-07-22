import os
from dotenv import load_dotenv
load_dotenv()
import json
import asyncio
import re
from typing import Dict, Any, List
from groq import AsyncGroq
from rag import retrieve_context
from tools.web_search import web_search

# Initialize Groq Client
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
try:
    groq_client = AsyncGroq(api_key=GROQ_API_KEY)
except Exception:
    groq_client = None

# Global in-memory storage for traces
# Format: { run_id: {"goal": str, "plan": [str], "steps": [{"step": str, "tool_used": str, "input": any, "output": any}], "final_result": str, "self_check": str, "status": "running" | "completed" | "failed", "error": str} }
global_traces: Dict[str, Dict[str, Any]] = {}

async def call_llama(messages, tools=None, model="llama-3.1-8b-instant"):
    if not groq_client:
        raise Exception("Groq client not initialized")
    
    kwargs = {"model": model, "messages": messages}
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    response = await groq_client.chat.completions.create(**kwargs)
    return response.choices[0].message

# --- Tools implementation ---
def search_documents(query: str) -> str:
    contexts = retrieve_context(query, n_results=3)
    if not contexts:
        return "No relevant documents found."
    results = []
    for ctx in contexts:
        results.append(f"Document: {ctx['filename']}\nContent: {ctx['text']}")
    return "\n\n---\n\n".join(results)

async def summarize_text(text: str) -> str:
    messages = [
        {"role": "system", "content": "You are a summarizing agent. Summarize the following text concisely."},
        {"role": "user", "content": text}
    ]
    resp = await call_llama(messages)
    return resp.content

async def draft_message(context: str, purpose: str) -> str:
    messages = [
        {"role": "system", "content": "You are an assistant that drafts messages or emails based on provided context and purpose."},
        {"role": "user", "content": f"Context:\n{context}\n\nPurpose:\n{purpose}\n\nPlease draft the message."}
    ]
    resp = await call_llama(messages)
    return resp.content

# --- Tool registry ---
TOOLS_DEF = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Searches the existing knowledge base for relevant documents. Use this to find company policies, guidelines, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query to look up"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_text",
            "description": "Summarizes a given long text into key points.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The long text to summarize"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "draft_message",
            "description": "Drafts an email or message using the given context and purpose.",
            "parameters": {
                "type": "object",
                "properties": {
                    "context": {"type": "string", "description": "The background context to include"},
                    "purpose": {"type": "string", "description": "The goal or purpose of the message"}
                },
                "required": ["context", "purpose"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "brave_search",
            "description": "Searches the web for current events, news, latest information, or facts outside the existing knowledge base, or when the user explicitly requests a web search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The web search query to look up"}
                },
                "required": ["query"]
            }
        }
    }
]

async def run_agent_loop(run_id: str, goal: str, language: str = "english", mode: str = "normal"):
    trace = {
        "goal": goal,
        "plan": [],
        "steps": [],
        "final_result": None,
        "self_check": None,
        "status": "running"
    }
    global_traces[run_id] = trace
    
    try:
        # Set up language prompt
        lang_str = "Hinglish (a mix of Hindi and English using Latin/Roman script)" if language.lower() == "hinglish" else "English"
        
        if mode == "normal":
            trace["steps"].append({"step": "Direct Completion", "tool_used": "None", "input": goal, "output": "Retrieving context and generating response..."})
            
            # Retrieve RAG context if applicable
            contexts = retrieve_context(goal, n_results=3)
            system_content = (
                f"You are Doxa, a helpful AI assistant. Answer the user's query directly and naturally in {lang_str}.\n"
                "Keep your response concise, conversational, and suitable for Text-to-Speech playback (avoid complex formatting, markdown tables, long lists, or code blocks).\n"
            )
            if contexts:
                system_content += "\nHere is some context from our knowledge base that might help:\n"
                system_content += "\n\n".join([f"Document: {c['filename']}\nContent: {c['text']}" for c in contexts])
            
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": goal}
            ]
            
            resp = await call_llama(messages, model="llama-3.3-70b-versatile")
            final_result = (resp.content or "Empty response generated.").strip()
            
            trace["final_result"] = final_result
            trace["steps"].append({"step": "Finalizing", "tool_used": "None", "input": "None", "output": "Completed direct response."})
            trace["status"] = "completed"
            return

        # Step 1: Planning (Agentic Mode)
        trace["steps"].append({"step": "Planning", "tool_used": "None", "input": goal, "output": "Generating plan..."})
        plan_messages = [
            {"role": "system", "content": f"You are a planning agent. Break this goal into 3-5 concrete steps. Output ONLY a valid JSON list of strings, e.g. [\"Step 1: ...\", \"Step 2: ...\"]. Do not output markdown code blocks. Respond in {lang_str}."},
            {"role": "user", "content": f"Goal: {goal}"}
        ]
        plan_msg = await call_llama(plan_messages)
        try:
            content = (plan_msg.content or "").strip()
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()
            plan = json.loads(content)
            if not isinstance(plan, list):
                plan = [plan_msg.content or "No plan generated"]
        except Exception:
            plan = [plan_msg.content or "No plan generated"]
            
        trace["plan"] = plan
        trace["steps"][-1]["output"] = "Plan generated."

        # Step 2: Execution (Agentic Mode)
        agent_messages = [
            {
                "role": "system", 
                "content": f"You are an AI assistant executing a plan to achieve a goal.\nGoal: {goal}\nPlan:\n" + "\n".join(plan) + f"\n\nUse the provided tools to execute the steps via standard function calling. When you need up-to-date facts, news, or latest events (e.g. 'today', 'latest', 'recent') or when explicitly asked to search the web, use the 'brave_search' tool. IMPORTANT: When you use 'brave_search', naturally integrate the findings into your final response and cite the sources/URLs. When you have enough information, write the final result directly to the user and DO NOT call any more tools. IMPORTANT: Your final response must be clean, natural language in {lang_str}. DO NOT include any tool call syntax, XML tags, or raw JSON in your final response."
            },
            {"role": "user", "content": "Begin execution."}
        ]
        
        final_result = None
        max_iterations = 8
        
        for _ in range(max_iterations):
            msg = await call_llama(agent_messages, tools=TOOLS_DEF, model="llama-3.3-70b-versatile")
            
            # The API might not return a dictionary but an object, so we convert appropriately or append directly.
            # groq Python client message object can be appended back to messages.
            agent_messages.append(msg)
            
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    step_record = {
                        "step": f"Executing {func_name}",
                        "tool_used": func_name,
                        "input": args,
                        "output": "Running..."
                    }
                    trace["steps"].append(step_record)
                    
                    tool_output = ""
                    try:
                        if func_name == "search_documents":
                            tool_output = search_documents(args.get("query", ""))
                        elif func_name == "summarize_text":
                            tool_output = await summarize_text(args.get("text", ""))
                        elif func_name == "draft_message":
                            tool_output = await draft_message(args.get("context", ""), args.get("purpose", ""))
                        elif func_name == "brave_search":
                            tool_output = web_search(args.get("query", ""))
                        else:
                            tool_output = f"Unknown tool: {func_name}"
                    except Exception as ex:
                        tool_output = f"Error executing tool: {ex}"
                        
                    step_record["output"] = tool_output[:1000] + ("..." if len(tool_output) > 1000 else "")
                    
                    agent_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": func_name,
                        "content": tool_output
                    })
            else:
                final_result = msg.content or "Agent generated empty response."
                
                # Regex filter to strip leaked tool-call hallucination syntax
                final_result = re.sub(r'<[\w_]+>\s*\{.*?\}\s*</[\w_]+>', '', final_result, flags=re.DOTALL)
                final_result = re.sub(r'={1,2}[\w_]+>\s*\{.*?\}', '', final_result, flags=re.DOTALL)
                final_result = final_result.strip()
                
                if not final_result:
                    final_result = "Agent completed execution but the final response was empty after filtering."
                    
                trace["final_result"] = final_result
                trace["steps"].append({"step": "Finalizing", "tool_used": "None", "input": "None", "output": "Generated final result."})
                break
                
        if not final_result:
            final_result = "Agent stopped without a final result (max iterations reached)."
            trace["final_result"] = final_result

        # Step 3: Self-Check
        trace["steps"].append({"step": "Self Check", "tool_used": "None", "input": final_result, "output": "Checking..."})
        check_messages = [
            {"role": "system", "content": "You are an evaluator. Review the final result against the original goal. Identify any missing parts or state if it is complete. Be brief and objective."},
            {"role": "user", "content": f"Goal: {goal}\n\nFinal Result:\n{final_result}\n\nSelf-check analysis:"}
        ]
        check_msg = await call_llama(check_messages)
        trace["self_check"] = check_msg.content
        trace["steps"][-1]["output"] = "Self-check complete."
        
        trace["status"] = "completed"
        
    except Exception as e:
        trace["status"] = "failed"
        trace["error"] = str(e)
