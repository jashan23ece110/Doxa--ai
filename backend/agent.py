import os
from dotenv import load_dotenv
load_dotenv()
import json
import asyncio
import re
from typing import Dict, Any, List
from groq import AsyncGroq
from google.cloud import firestore
from rag import retrieve_context
from tools.web_search import web_search
from tools.calculator import calculate

# Initialize Groq Client
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
try:
    groq_client = AsyncGroq(api_key=GROQ_API_KEY)
except Exception:
    groq_client = None

# Global in-memory storage fallback for local dev
global_traces: Dict[str, Dict[str, Any]] = {}

# Initialize Firestore client
try:
    # Use project environment variable or auto-detect
    db = firestore.Client()
except Exception as e:
    print(f"Firestore not initialized (using memory fallback): {e}")
    db = None

def save_trace(run_id: str, trace: dict):
    global_traces[run_id] = trace
    if db:
        try:
            db.collection("traces").document(run_id).set(trace)
        except Exception as e:
            print(f"Error saving to Firestore: {e}")

def get_trace(run_id: str) -> dict:
    if db:
        try:
            doc = db.collection("traces").document(run_id).get()
            if doc.exists:
                return doc.to_dict()
        except Exception as e:
            print(f"Error getting from Firestore: {e}")
    return global_traces.get(run_id)

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
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluates basic mathematical and trigonometric expressions safely. Use this for math, logic, or calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "The mathematical expression to evaluate, e.g. 'sin(pi/2) * 5' or '4529 * 93'"}
                },
                "required": ["expression"]
            }
        }
    }
]

async def run_agent_loop(run_id: str, goal: str, language: str = "english", mode: str = "normal", history: List[dict] = None):
    trace = {
        "goal": goal,
        "plan": [],
        "steps": [],
        "final_result": None,
        "self_check": None,
        "status": "running"
    }
    save_trace(run_id, trace)
    
    try:
        # Set up language prompt
        lang_str = "Hinglish (a mix of Hindi and English using Latin/Roman script)" if language.lower() == "hinglish" else "English"
        
        if mode == "normal":
            trace["steps"].append({"step": "Direct Completion", "tool_used": "None", "input": goal, "output": "Retrieving context and generating response..."})
            save_trace(run_id, trace)
            
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
                {"role": "system", "content": system_content}
            ]
            if history:
                for h in history:
                    messages.append({"role": h.get("role", "user"), "content": h.get("text", "")})
            messages.append({"role": "user", "content": goal})
            
            import time
            response_stream = await groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.1,
                stream=True
            )
            
            trace["final_result"] = ""
            last_save = 0
            async for chunk in response_stream:
                delta_content = chunk.choices[0].delta.content or ""
                trace["final_result"] += delta_content
                now = time.time()
                if now - last_save > 0.25:
                    save_trace(run_id, trace)
                    last_save = now
            
            trace["final_result"] = trace["final_result"].strip()
            trace["steps"].append({"step": "Finalizing", "tool_used": "None", "input": "None", "output": "Completed direct response."})
            trace["status"] = "completed"
            save_trace(run_id, trace)
            return

        # Step 1: Planning (Agentic Mode)
        trace["steps"].append({"step": "Planning", "tool_used": "None", "input": goal, "output": "Generating plan..."})
        save_trace(run_id, trace)
        
        plan_messages = [
            {"role": "system", "content": f"You are a planning agent. Break this goal into 3-5 concrete steps. Output ONLY a valid JSON list of strings, e.g. [\"Step 1: ...\", \"Step 2: ...\"]. Do not output markdown code blocks. Respond in {lang_str}."}
        ]
        if history:
            for h in history:
                plan_messages.append({"role": h.get("role", "user"), "content": h.get("text", "")})
        plan_messages.append({"role": "user", "content": f"Goal: {goal}"})
        
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
        save_trace(run_id, trace)

        # Step 2: Execution (Agentic Mode)
        agent_messages = [
            {
                "role": "system", 
                "content": f"You are an AI assistant executing a plan to achieve a goal.\nGoal: {goal}\nPlan:\n" + "\n".join(plan) + f"\n\nUse the provided tools to execute the steps via standard function calling. When you need up-to-date facts, news, or latest events (e.g. 'today', 'latest', 'recent') or when explicitly asked to search the web, use the 'brave_search' tool. To calculate mathematical expressions, use the 'calculate' tool. IMPORTANT: When you use 'brave_search', naturally integrate the findings into your final response and cite the sources/URLs. When you have enough information, write the final result directly to the user and DO NOT call any more tools. IMPORTANT: Your final response must be clean, natural language in {lang_str}. DO NOT include any tool call syntax, XML tags, or raw JSON in your final response."
            }
        ]
        if history:
            for h in history:
                agent_messages.append({"role": h.get("role", "user"), "content": h.get("text", "")})
        agent_messages.append({"role": "user", "content": "Begin execution."})
        
        final_result = None
        max_iterations = 8
        retry_count = 0
        
        while retry_count < 2:
            iteration_count = 0
            for _ in range(max_iterations):
                iteration_count += 1
                msg = await call_llama(agent_messages, tools=TOOLS_DEF, model="llama-3.3-70b-versatile")
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
                        save_trace(run_id, trace)
                        
                        tool_output = ""
                        try:
                            if func_name == "search_documents":
                                tool_output = await search_documents(args.get("query", ""))
                            elif func_name == "summarize_text":
                                tool_output = await summarize_text(args.get("text", ""))
                            elif func_name == "draft_message":
                                tool_output = await draft_message(args.get("context", ""), args.get("purpose", ""))
                            elif func_name == "brave_search":
                                tool_output = web_search(args.get("query", ""))
                            elif func_name == "calculate":
                                tool_output = calculate(args.get("expression", ""))
                            else:
                                tool_output = f"Unknown tool: {func_name}"
                        except Exception as ex:
                            tool_output = f"Error executing tool: {ex}"
                            
                        step_record["output"] = tool_output[:1000] + ("..." if len(tool_output) > 1000 else "")
                        save_trace(run_id, trace)
                        
                        agent_messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": func_name,
                            "content": tool_output
                        })
                else:
                    final_result = msg.content or "Agent generated empty response."
                    final_result = re.sub(r'<[\w_]+>\s*\{.*?\}\s*</[\w_]+>', '', final_result, flags=re.DOTALL)
                    final_result = re.sub(r'={1,2}[\w_]+>\s*\{.*?\}', '', final_result, flags=re.DOTALL)
                    final_result = final_result.strip()
                    
                    if not final_result:
                        final_result = "Agent completed execution but the final response was empty after filtering."
                        
                    trace["final_result"] = final_result
                    trace["steps"].append({"step": "Finalizing", "tool_used": "None", "input": "None", "output": "Generated final result."})
                    save_trace(run_id, trace)
                    break
                    
            if not final_result:
                final_result = "Agent stopped without a final result (max iterations reached)."
                trace["final_result"] = final_result
                save_trace(run_id, trace)

            # Step 3: Self-Check with retry triggers
            trace["steps"].append({"step": "Self Check", "tool_used": "None", "input": final_result, "output": "Checking..."})
            save_trace(run_id, trace)
            
            check_messages = [
                {"role": "system", "content": "You are an evaluator. Review the final result against the original goal. Output '[MET]' if the goal is fully and correctly achieved, or '[NOT_MET]' if some requirements are missing. Write a brief, objective analysis (1-2 sentences)."},
                {"role": "user", "content": f"Goal: {goal}\n\nFinal Result:\n{final_result}\n\nSelf-check analysis:"}
            ]
            check_msg = await call_llama(check_messages)
            check_content = check_msg.content or ""
            trace["self_check"] = check_content
            trace["steps"][-1]["output"] = "Self-check complete."
            save_trace(run_id, trace)
            
            if "[NOT_MET]" in check_content and retry_count == 0:
                retry_count += 1
                trace["steps"].append({
                    "step": "Retrying", 
                    "tool_used": "None", 
                    "input": "Self-check failure", 
                    "output": f"Retry #{retry_count} triggered due to: {check_content}"
                })
                save_trace(run_id, trace)
                
                # Feedback loop: append self-check critique and retry execution
                agent_messages.append({
                    "role": "user", 
                    "content": f"Self-check critique: The goal was NOT MET. Reason: {check_content}. Please refine your execution and deliver a completed result."
                })
                final_result = None
            else:
                break
                
        trace["status"] = "completed"
        save_trace(run_id, trace)
        
    except Exception as e:
        trace["status"] = "failed"
        trace["error"] = str(e)
        save_trace(run_id, trace)
