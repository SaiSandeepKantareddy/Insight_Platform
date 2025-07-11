# Insight Platform — AI Signal Connector Prototype

> **Modular Agentic System for Curated AI Insights Using LangGraph + Ollama**

---

## What This Is

A modular Python project combining:

- **LangGraph Agent Flow:**  
  Scraper → Summarizer → Tagger → Connector → Publisher  
- **Ollama for Local Summarization:**  
  Using `/api/generate` endpoint with streamed response handling  
- **Streamlit UI for End-User Display:**  
  Browse markdown-formatted insights with tags and source URLs  
- **Markdown + JSON File Storage:**  
  Insights saved as `.md` + `.meta.json` pairs  

---

## Project Structure

```
backend/
├── app.py (FastAPI routes)
├── core/orchestrator.py (LangGraph flow)
├── agents/ (scraper_agent, summarizer_agent, etc.)
├── protocols/ (mcp, a2a, acp structures)
├── utils/
streamlit_ui/
├── app.py (Streamlit frontend)
docker-compose.yml
README.md
```

---

## How to Set Up Locally

### Clone the Repo

```bash
git clone https://github.com/yourusername/insight-platform.git
cd insight-platform
```

### Pull Required Ollama Model

Start only Ollama service first:

```bash
docker compose up ollama
```

Then pull the model:

```bash
curl -X POST http://localhost:11434/api/pull \
  -H "Content-Type: application/json" \
  -d '{"name": "llama3"}'
```

### Build and Run Backend + UI

```bash
docker compose up --build
```

- Backend available at: `http://localhost:8000`
- Streamlit UI at: `http://localhost:8501`

---

## Workflow Summary

1. Send a URL to `/run_pipeline`:
   - The pipeline scrapes → summarizes → tags → connects → publishes.
2. Visit Streamlit UI or call `/list_insights` API to view insights.
3. Insights include:
   - Title, tags, content preview, original source URL.

---

## Current Scope + Limitations

- No CI/CD or Kubernetes deployment yet.
- Models must be pulled manually the first time.
- Local file storage only; no database integration yet.

---

## Future Enhancements

- [ ] CI/CD pipelines (GitHub Actions, Docker Registry)
- [ ] Full Kubernetes Helm Charts
- [ ] OAuth2 login on Streamlit UI
- [ ] Ollama model pre-pull automation

---

## Contribution Guidelines

- Fork → Clone → Submit PR  
- Focus on modular, readable, community-friendly code.
