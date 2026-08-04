# Graph Report - .  (2026-08-01)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 246 nodes · 369 edges · 20 communities (18 shown, 2 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.64)
- Token cost: 704 input · 45 output

## Graph Freshness
- Built from commit: `102f3a2f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Agent API Endpoints
- Agent Logic and RAG
- UI Components and Animations
- Frontend Dependencies
- rag.py
- Dashboard.jsx
- devDependencies
- deploy
- .oxlintrc.json
- execute_python_code
- Backend Dependencies
- Cloud Build Configuration
- Frontend Entry Point
- Acme Corp Employee Handbook
- Hero Illustration

## God Nodes (most connected - your core abstractions)
1. `run_agent_loop()` - 25 edges
2. `react` - 16 edges
3. `add_document()` - 12 edges
4. `get_trace()` - 10 edges
5. `retrieve_context()` - 9 edges
6. `evaluate_prompt()` - 7 edges
7. `start_agent()` - 6 edges
8. `get_chroma_collection()` - 6 edges
9. `delete_document()` - 6 edges
10. `execute_python_code()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `run_agent_loop()`  [EXTRACTED]
  test_agent.py → backend/agent.py
- `start_agent()` --indirect_call--> `run_agent_loop()`  [INFERRED]
  backend/main.py → backend/agent.py
- `Acme Corp Employee Handbook` --semantically_similar_to--> `Professional Resume Writing Guide`  [INFERRED] [semantically similar]
  backend/sample_docs/company_policy.txt → backend/sample_docs/resume_guide.txt
- `Frontend Entry Point` --references--> `Doxa Logo`  [EXTRACTED]
  frontend/index.html → frontend/public/favicon.svg
- `get_agent_status()` --calls--> `get_trace()`  [EXTRACTED]
  backend/main.py → backend/agent.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Backend Technology Stack** — fastapi, chromadb, openai, backend_requirements [EXTRACTED 0.90]
- **CI/CD Deployment Flow** — backend_cloudbuild, doxa_backend_container, google_cloud_run [EXTRACTED 1.00]

## Communities (20 total, 2 thin omitted)

### Community 0 - "Agent API Endpoints"
Cohesion: 0.08
Nodes (37): AgentRequest, call_groq(), create_timer(), evaluate_prompt(), EvaluateRequest, get_agent_status(), get_documents(), get_proactive_suggestions() (+29 more)

### Community 1 - "Agent Logic and RAG"
Cohesion: 0.11
Nodes (31): Any, call_tokenrouter(), classify_sentiment(), draft_message(), get_trace(), run_agent_loop(), save_trace(), search_documents() (+23 more)

### Community 2 - "UI Components and Animations"
Cohesion: 0.11
Nodes (20): App(), cardHover, hoverScale, pageVariants, staggerContainer, staggerItem, tapScale, ChatPanel() (+12 more)

### Community 3 - "Frontend Dependencies"
Cohesion: 0.07
Nodes (26): axios, framer-motion, dependencies, axios, framer-motion, lucide-react, react, react-dom (+18 more)

### Community 4 - "rag.py"
Cohesion: 0.11
Nodes (24): Delete a document and all its chunks from the knowledge base., remove_document(), add_document(), chunk_text(), _delete_chunks_by_doc_id(), delete_document(), extract_text_from_file(), generate_doc_id() (+16 more)

### Community 5 - "Dashboard.jsx"
Cohesion: 0.11
Nodes (17): CentralCore(), extractMorphKeyword(), ParticleSwarm(), sampleTextToPoints(), Dashboard(), fadeIn, slideUp, ObjectivesCard() (+9 more)

### Community 6 - "devDependencies"
Cohesion: 0.11
Nodes (19): autoprefixer, devDependencies, autoprefixer, oxlint, postcss, tailwindcss, @tailwindcss/postcss, @types/react (+11 more)

### Community 7 - "deploy"
Cohesion: 0.22
Nodes (8): build, builder, deploy, healthcheckPath, restartPolicyMaxRetries, restartPolicyType, startCommand, $schema

### Community 8 - ".oxlintrc.json"
Cohesion: 0.25
Nodes (7): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, oxc, warn

### Community 9 - "execute_python_code"
Cohesion: 0.47
Nodes (5): execute_python_code(), Executes a snippet of Python code in a restricted sandbox process. Times out…, Worker function meant to run inside a separate, isolated process. Redirects…, _run_in_sandbox(), Queue

### Community 10 - "Backend Dependencies"
Cohesion: 0.50
Nodes (4): Backend Dependencies, ChromaDB, FastAPI, OpenAI

### Community 11 - "Cloud Build Configuration"
Cohesion: 0.67
Nodes (3): Cloud Build Configuration, Doxa Backend Container, Google Cloud Run

### Community 12 - "Frontend Entry Point"
Cohesion: 0.67
Nodes (3): Frontend Entry Point, Doxa Logo, Frontend README

## Knowledge Gaps
- **53 isolated node(s):** `$schema`, `builder`, `startCommand`, `healthcheckPath`, `restartPolicyType` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_agent_loop()` connect `Agent Logic and RAG` to `Agent API Endpoints`, `execute_python_code`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `react` connect `UI Components and Animations` to `.oxlintrc.json`, `Dashboard.jsx`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `devDependencies` connect `devDependencies` to `Frontend Dependencies`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **What connects `$schema`, `builder`, `startCommand` to the rest of the system?**
  _53 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Agent API Endpoints` be split into smaller, more focused modules?**
  _Cohesion score 0.08232118758434548 - nodes in this community are weakly interconnected._
- **Should `Agent Logic and RAG` be split into smaller, more focused modules?**
  _Cohesion score 0.11379800853485064 - nodes in this community are weakly interconnected._
- **Should `UI Components and Animations` be split into smaller, more focused modules?**
  _Cohesion score 0.10804597701149425 - nodes in this community are weakly interconnected._