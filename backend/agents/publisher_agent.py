import os,json
from datetime import datetime

# def publish_markdown(summary: str, tags: list, insight: str, source_url:str,path="data/output") -> str:
#     os.makedirs(path, exist_ok=True)
#     date_str = datetime.now().strftime("%Y-%m-%d")
#     filename = f"{path}/signal_{date_str}.md"

#     content = f"""\n# Insight — {date_str}\n\n{summary}\n\n**Tags:** {', '.join(tags)}\n\n {insight}\n\n---\n\n **source_url:**\n\n {source_url}\n"""
#     with open(filename, "w") as f:
#         f.write(content)
#     return filename


def publish_markdown(summary: str, tags: list, insight: str, source_url: str, path="data/output") -> str:
    os.makedirs(path, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename_base = f"{path}/signal_{date_str}"
    md_filename = f"{filename_base}.md"
    meta_filename = f"{filename_base}.meta.json"

    content = f"""
# Insight — {date_str}

{summary}

**Tags:** {', '.join(tags)}

{insight}

---

**source_url:**

{source_url}
"""
    with open(md_filename, "w") as f:
        f.write(content)

    meta = {
        "source_url": source_url,
        "tags": tags
    }
    with open(meta_filename, "w") as meta_file:
        json.dump(meta, meta_file)

    return md_filename