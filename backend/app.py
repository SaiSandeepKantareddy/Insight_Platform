
from requests import Response
from core.orchestrator import build_graph
from fastapi import FastAPI, Request
import os
import glob
import json, uvicorn

# if __name__ == "__main__":
#     graph = build_graph()

#     url = "https://deepmind.google/discover/blog/alphagenome-ai-for-better-understanding-the-genome/"
#     initial_state = { "url": url }

#     final_state = graph.invoke(initial_state)
#     print(f"Insight published to: {final_state.get('output_path')}")


app = FastAPI()
graph = build_graph()

@app.post("/run_pipeline")
async def run_pipeline(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return {"error": "Missing URL"}
    result = graph.invoke({"url": url})
    return {"result": result}

@app.get("/list_insights")
def list_insights():
    output_dir = "data/output"
    files = sorted(glob.glob(f"{output_dir}/*.md"))
    insights = []
    for file_path in files[-5:]:  # Only latest 5
        with open(file_path) as f:
            content = f.read()

        meta_path = file_path.replace(".md", ".meta.json")
        if os.path.exists(meta_path):
            with open(meta_path) as meta_file:
                meta = json.load(meta_file)
            tags = meta.get("tags", ["sample"])
            source_url = meta.get("source_url", "https://example.com")
        else:
            tags = ["sample"]
            source_url = "https://example.com"

        insights.append({
            "title": os.path.basename(file_path),
            "summary": content[:500] + "...",
            "tags": tags,
            "source_url": source_url
        })
    return {"insights": insights}

@app.get("/logs/protocols")
def download_logs():
    log_path = "logs/protocol_trace.json"
    if os.path.exists(log_path):
        with open(log_path, "rb") as f:
            return Response(f.read(), media_type="application/json")
    else:
        return {"error": "No logs available."}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
