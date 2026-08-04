<p align="center">
  <img src="frontend/src/assets/logo.png" width="120" alt="Doxa AI Logo" />
</p>

<h1 align="center">Doxa AI — Autonomous Agent Platform & RAG Pipeline</h1>

<p align="center">
  <b>Meet Doxa — An AI that thinks, searches, and acts.</b><br />
  Autonomous multi-step reasoning, vector RAG document intelligence, live web citations, and native voice mode.
</p>

---

## ⚡ Features

- 🤖 **Autonomous Multi-Step Agent Loop**: Planning, tool execution, intermediate reasoning, and self-critique.
- 📚 **Vector RAG Knowledge Base**: Upload PDFs, text, and markdown files stored in persistent ChromaDB vector storage.
- 🌐 **Live Web Search**: Tavily-powered real-time web search and citation grounding.
- 🎙️ **Native Voice Mode**: Continuous Web Speech API wake-phrase detection and voice synthesis.
- 💬 **LibreChat-Inspired Workspace**: Grouped conversation history, model selector dropdown, message action toolbars, and non-linear thread branching.
- ⚡ **Sub-50ms Low-Latency Token Streaming**: Fast continuous token delivery.

---

## 🚀 Quick Start

### 1. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

---

## 🎨 Tech Stack

- **Frontend**: React, Vite, Tailwind CSS, Framer Motion, Three.js
- **Backend**: FastAPI, ChromaDB, Sentence Transformers, TokenRouter (Moonshot Kimi-K3)
- **Deployment**: Vercel (Frontend), Daytona Sandboxes (Backend)
