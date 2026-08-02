import os
from dotenv import load_dotenv
load_dotenv()
import json
import asyncio
import re
import uuid
import time
from typing import Dict, Any, List

from openai import AsyncOpenAI, RateLimitError, APIError

from google.cloud import firestore
from rag import retrieve_context
from tools.web_search import web_search
from tools.calculator import calculate
from tools.calendar_tool import list_calendar_events, create_calendar_event
from tools.python_sandbox import execute_python_code
from tools.timer_manager import schedule_timer

# Configure TokenRouter API Client
TOKENROUTER_API_KEY = os.getenv("TOKENROUTER_API_KEY", "")
TOKENROUTER_BASE_URL = os.getenv("TOKENROUTER_BASE_URL", "https://api.tokenrouter.com/v1")
DEFAULT_MODEL = os.getenv("TOKENROUTER_MODEL", "moonshotai/kimi-k3-free")

if TOKENROUTER_API_KEY:
    print("TokenRouter API client configured successfully.")
else:
    print("Warning: TOKENROUTER_API_KEY is not set.")

client = AsyncOpenAI(
    api_key=TOKENROUTER_API_KEY if TOKENROUTER_API_KEY else "dummy_key",
    base_url=TOKENROUTER_BASE_URL
)

# Global in-memory storage fallback for local dev
global_traces: Dict[str, Dict[str, Any]] = {}

# Initialize Firestore client
try:
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

def classify_sentiment(text: str) -> str:
    text_lower = text.lower()
    exciting_keywords = ["congrats", "congratulations", "excellent", "great", "awesome", "win", "excited", "happy", "yes!", "cool", "amazing", "beautiful", "wonderful", "celebrate", "perfect", "wow", "fantastic", "superb", "yay", "mubarak", "badhiya", "shandar", "zabardast"]
    sad_serious_keywords = ["fail", "failed", "failure", "lost", "die", "death", "sad", "grave", "catastrophe", "wrong", "accident", "bad", "sorry", "condolences", "regret", "apologize", "unfortunate", "grief", "cancel", "error", "warning", "critical", "severe", "fatal", "khabar kharab", "nuksan", "maut", "dukh", "chinta"]
    
    exciting_count = sum(1 for w in exciting_keywords if w in text_lower)
    sad_count = sum(1 for w in sad_serious_keywords if w in text_lower)
    
    if exciting_count > sad_count:
        return "exciting"
    elif sad_count > exciting_count:
        return "serious"
    return "neutral"

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
    resp = await call_tokenrouter(messages)
    return resp.content

async def draft_message(context: str, purpose: str) -> str:
    messages = [
        {"role": "system", "content": "You are an assistant that drafts messages or emails based on provided context and purpose."},
        {"role": "user", "content": f"Context:\n{context}\n\nPurpose:\n{purpose}\n\nPlease draft the message."}
    ]
    resp = await call_tokenrouter(messages)
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
    },
    {
        "type": "function",
        "function": {
            "name": "list_calendar_events",
            "description": "Lists upcoming events and meetings from the user's primary calendar.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "Creates a new calendar event or meeting. Time parameter is best provided in ISO format (e.g. 2026-07-25T14:00:00).",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string", "description": "The event title or name"},
                    "start_time": {"type": "string", "description": "The starting date/time of the event, preferred in ISO format (e.g., 2026-07-25T10:30:00)"},
                    "duration_minutes": {"type": "integer", "description": "The duration of the event in minutes (default 30)"},
                    "description": {"type": "string", "description": "Optional description or meeting agenda"}
                },
                "required": ["summary", "start_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python_code",
            "description": "Runs a script of Python code safely in a restricted sandbox process and returns its standard output/error. Ideal for algorithms, sorting, complex loops, string processing, or multi-step logic. No imports, file operations, or network calls are allowed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "The Python code block to execute"}
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_timer",
            "description": "Sets an in-app alarm or reminder timer for a specific duration.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The reminder label or reason for the timer"},
                    "duration_seconds": {"type": "integer", "description": "The duration of the timer in seconds (e.g., 300 for 5 minutes, 60 for 1 minute)"}
                },
                "required": ["title", "duration_seconds"]
            }
        }
    }
]

async def call_tokenrouter(messages: List[dict], tools: List[dict] = None, model: str = None) -> Any:
    target_model = model or DEFAULT_MODEL
    if target_model in ["gemini-2.0-flash", "gemini-2.0-flash-001", "gemini-1.5-flash", "llama-3.1-8b-instant"]:
        target_model = "moonshotai/kimi-k3-free"

    kwargs = {
        "model": target_model,
        "messages": messages,
        "temperature": 0.1
    }
    if tools:
        kwargs["tools"] = tools

    max_retries = 3
    delay = 2.0

    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(**kwargs)
            return response.choices[0].message
        except RateLimitError as e:
            print(f"TokenRouter API rate limit hit (RateLimitError) on attempt {attempt+1}/{max_retries}. Retrying in {delay}s...")
            if attempt == max_retries - 1:
                raise Exception("TokenRouter API rate limit exceeded. Please try again after a moment.") from e
            await asyncio.sleep(delay)
            delay *= 2
        except Exception as e:
            err_msg = str(e).lower()
            is_rate_limit = any(x in err_msg for x in ["429", "rate_limit", "ratelimit", "resource_exhausted"])
            if is_rate_limit:
                print(f"TokenRouter API rate limit hit on attempt {attempt+1}/{max_retries}. Retrying in {delay}s...")
                if attempt == max_retries - 1:
                    raise Exception("TokenRouter API rate limit exceeded. Please try again after a moment.") from e
                await asyncio.sleep(delay)
                delay *= 2
            else:
                print(f"TokenRouter API error calling {target_model}: {e}")
                raise e

# Compatibility aliases
call_gemini = call_tokenrouter
call_llama = call_tokenrouter

async def run_agent_loop(run_id: str, goal: str, language: str = "english", mode: str = "normal", history: List[dict] = None):
    trace = {
        "goal": goal,
        "plan": [],
        "steps": [],
        "final_result": None,
        "self_check": None,
        "sentiment": "neutral",
        "is_debating": False,
        "debate_a": "",
        "debate_b": "",
        "status": "running"
    }
    save_trace(run_id, trace)
    
    try:
        lang_str = "Hinglish (a mix of Hindi and English using Latin/Roman script)" if language.lower() == "hinglish" else "English"
        
        debatable_keywords = ["should i", "which is better", "what's better", "compare", "vs", "versus", "debate", "opinion", "pros and cons", "should we", "should they", "is it good", "advantages and disadvantages", "kya mujhe", "kaunsa accha hai"]
        is_debatable = any(kw in goal.lower() for kw in debatable_keywords)
        
        if is_debatable:
            trace["is_debating"] = True
            trace["steps"].append({"step": "Debate Mode Triggered", "tool_used": "DebateEngine", "input": goal, "output": "Initiating parallel debate between Agent Optimist and Agent Skeptic..."})
            save_trace(run_id, trace)
            
            prompt_a = [
                {"role": "system", "content": f"You are Agent Optimist. Argue STRONGLY in favor of the idea, focusing on pros, advantages, and benefits. Write a clear, brief perspective (2-4 sentences) in {lang_str}."},
                {"role": "user", "content": f"Topic: {goal}"}
            ]
            prompt_b = [
                {"role": "system", "content": f"You are Agent Skeptic. Argue STRONGLY against the idea, highlighting risks, cons, challenges, and concerns. Write a clear, brief perspective (2-4 sentences) in {lang_str}."},
                {"role": "user", "content": f"Topic: {goal}"}
            ]
            
            msg_a, msg_b = await asyncio.gather(
                call_tokenrouter(prompt_a),
                call_tokenrouter(prompt_b)
            )
            
            res_a = msg_a.content or "No argument generated."
            res_b = msg_b.content or "No counter-argument generated."
            
            trace["debate_a"] = res_a
            trace["debate_b"] = res_b
            trace["steps"].append({"step": "Synthesizing Perspectives", "tool_used": "DebateEngine", "input": "Consolidating perspectives", "output": "Drafting balanced synthesis..."})
            save_trace(run_id, trace)
            
            prompt_synth = [
                {"role": "system", "content": f"You are Doxa. Synthesize this debate (Perspective A: Optimistic, Perspective B: Skeptical) into a single, balanced, cohesive final response in {lang_str}. Address the user directly, summarize both sides neutrally, and help them make a decision. Keep it concise."},
                {"role": "user", "content": f"Topic: {goal}\n\nPerspective A (Optimist):\n{res_a}\n\nPerspective B (Skeptic):\n{res_b}\n\nWrite the balanced final response:"}
            ]
            
            msg_synth = await call_tokenrouter(prompt_synth)
            final_result = msg_synth.content or "Synthesis failed."
            
            trace["final_result"] = final_result
            trace["sentiment"] = classify_sentiment(final_result)
            trace["is_debating"] = False
            trace["status"] = "completed"
            save_trace(run_id, trace)
            return
            
        chat_words = goal.strip().lower().replace("?", "").replace("!", "").replace(",", "").split()
        greetings = {"hi", "hello", "hey", "hola", "namaste", "greetings", "good morning", "good afternoon", "good evening", "howdy", "sup", "yo", "kaise ho"}
        is_simple_greeting = False
        if len(chat_words) <= 3:
            is_simple_greeting = any(w in greetings for w in chat_words)
            
        if is_simple_greeting:
            mode = "normal"

        if mode in ("normal", "ask"):
            trace["steps"].append({"step": "Direct Completion", "tool_used": "None", "input": goal, "output": "Retrieving context and generating response..."})
            save_trace(run_id, trace)
            
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
            
            # OpenAI streaming completions
            response_stream = None
            max_retries = 3
            delay = 2.0
            
            for attempt in range(max_retries):
                try:
                    response_stream = await client.chat.completions.create(
                        model=DEFAULT_MODEL,
                        messages=messages,
                        stream=True,
                        temperature=0.1
                    )
                    break
                except (RateLimitError, Exception) as e:
                    err_msg = str(e).lower()
                    is_rate_limit = isinstance(e, RateLimitError) or any(x in err_msg for x in ["429", "rate_limit", "ratelimit", "resource_exhausted"])
                    if is_rate_limit:
                        print(f"TokenRouter streaming rate limit hit on attempt {attempt+1}. Retrying in {delay}s...")
                        if attempt == max_retries - 1:
                            raise Exception("TokenRouter API rate limit exceeded. Please try again after a moment.")
                        await asyncio.sleep(delay)
                        delay *= 2
                    else:
                        raise e
            
            trace["final_result"] = ""
            last_save = 0
            async for chunk in response_stream:
                if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    delta_content = chunk.choices[0].delta.content
                    trace["final_result"] += delta_content
                    now = time.time()
                    if now - last_save > 0.25:
                        save_trace(run_id, trace)
                        last_save = now
            
            trace["final_result"] = trace["final_result"].strip()
            trace["sentiment"] = classify_sentiment(trace["final_result"])
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
        
        plan_msg = await call_tokenrouter(plan_messages)
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
                "content": (
                    f"You are Doxa, an advanced agentic AI assistant executing a plan to achieve a goal.\nGoal: {goal}\nPlan:\n" + "\n".join(plan) + 
                    f"\n\nUse your available tools to retrieve facts, search the web, execute Python code, manage calendar events, or perform calculations. "
                    "Note: Third-party integrations like WhatsApp messaging, Spotify control, and desktop automation are currently Coming Soon on the roadmap. "
                    "If the user asks for these, do not attempt to invoke any tool; simply state that these features are coming soon on the roadmap.\n\n"
                    f"When you have enough information, provide a natural and complete final response directly in {lang_str}. Cite sources/URLs when presenting search findings."
                )
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
                msg = await call_tokenrouter(agent_messages, tools=TOOLS_DEF)
                
                # Append assistant message to message list
                assistant_msg = {"role": "assistant", "content": msg.content}
                if msg.tool_calls:
                    assistant_msg["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in msg.tool_calls
                    ]
                agent_messages.append(assistant_msg)
                
                if msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        func_name = tool_call.function.name
                        args = json.loads(tool_call.function.arguments) if isinstance(tool_call.function.arguments, str) else tool_call.function.arguments
                        
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
                            elif func_name == "list_calendar_events":
                                tool_output = list_calendar_events()
                            elif func_name == "create_calendar_event":
                                tool_output = create_calendar_event(
                                    summary=args.get("summary", ""),
                                    start_time=args.get("start_time", ""),
                                    duration_minutes=int(args.get("duration_minutes", 30)),
                                    description=args.get("description", "")
                                )
                            elif func_name == "execute_python_code":
                                tool_output = execute_python_code(args.get("code", ""))
                            elif func_name == "set_timer":
                                tool_output = schedule_timer(
                                    title=args.get("title", ""),
                                    seconds=int(args.get("duration_seconds", 60))
                                )
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
                    trace["sentiment"] = classify_sentiment(final_result)
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
            check_msg = await call_tokenrouter(check_messages)
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
                
                agent_messages.append({
                    "role": "user", 
                    "content": f"Self-check critique: The goal was NOT MET. Reason: {check_content}. Please refine your execution and deliver a completed result."
                })
                final_result = None
            else:
                break
                
        # Safeguard check for raw planning / meta-text leak
        if trace.get("final_result"):
            red_flag_phrases = [
                "the goal is to", 
                "potential response could be", 
                "the plan to achieve", 
                "a potential response", 
                "steps to achieve", 
                "my planning is",
                "first step is to",
                "the context of the greeting",
                "responding to the greeting"
            ]
            has_leak = any(phrase in trace["final_result"].lower() for phrase in red_flag_phrases)
            
            if has_leak:
                trace["steps"].append({"step": "Safeguard Triggered", "tool_used": "SafeguardEngine", "input": "Meta-text detected", "output": "Re-synthesizing response to ensure directness..."})
                save_trace(run_id, trace)
                
                clean_messages = [
                    {"role": "system", "content": f"You are Doxa. The previous response was raw internal planning text. Rewrite it into a direct, natural, conversational final response in {lang_str}. Avoid meta-commentary, lists, or mentioning the plan/goal. Respond directly to the user's input: '{goal}'."},
                    {"role": "user", "content": f"Raw internal response: {trace['final_result']}\n\nDirect response:"}
                ]
                clean_msg = await call_tokenrouter(clean_messages)
                trace["final_result"] = (clean_msg.content or "").strip()
                trace["sentiment"] = classify_sentiment(trace["final_result"])
                save_trace(run_id, trace)

        trace["status"] = "completed"
        save_trace(run_id, trace)
        
    except Exception as e:
        trace["status"] = "failed"
        trace["error"] = str(e)
        save_trace(run_id, trace)
