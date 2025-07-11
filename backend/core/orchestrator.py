from langgraph.graph import StateGraph
from typing import TypedDict, Optional, List

from agents.scraper_agent import scrape_article
from agents.summarizer_agent import summarize_with_ollama
from agents.tagger_agent import basic_tagger
from agents.connector_agent import generate_dot_connection
from agents.publisher_agent import publish_markdown

# Protocols
from protocols.mcp import create_mcp_payload
from protocols.a2a import create_a2a_message
from protocols.acp import create_acp_message 


# Shared state
class SignalState(TypedDict):
    url: str
    article: Optional[dict]
    summary: Optional[str]
    tags: Optional[List[str]]
    insight: Optional[str]
    output_path: Optional[str]

# --- Agent Nodes ---

def scraper_node(state: SignalState) -> SignalState:
    print("[ScraperAgent] Scraping article...")
    article = scrape_article(state["url"])
    state["article"] = article
    print(f"[ScraperAgent] Scraped: {article['title'][:60]}")
    return state

def summarizer_node(state: SignalState) -> SignalState:
    print("[SummarizerAgent] Summarizing article using MCP protocol...")
    mcp = create_mcp_payload(
        goal="Summarize the article",
        context="Weekly AI insight for builders and analysts",
        input_text=state["article"]["text"],
        format_type="markdown"
    )
    summary = summarize_with_ollama(mcp["input"])
    state["summary"] = summary
    print(f"[SummarizerAgent] Summary done (chars: {len(summary)})")
    return state

def tagger_node(state: SignalState) -> SignalState:
    print("[TaggerAgent] Tagging summary...")
    tags = basic_tagger(state["summary"])
    state["tags"] = tags
    print(f"[TaggerAgent] Tags: {tags}")
    return state

def connector_node(state: SignalState) -> SignalState:
    print("🔗 [ConnectorAgent] Generating dot-connection insight using A2A...")
    a2a = create_a2a_message(
        sender="TaggerAgent",
        receiver="ConnectorAgent",
        task="Connect summary and tags into an insight",
        payload={"summary": state["summary"], "tags": state["tags"]}
    )
    print(f"[A2A] Message: {a2a}")
    insight = generate_dot_connection(a2a["payload"]["summary"])
    state["insight"] = insight
    print(f"[ConnectorAgent] Insight: {insight}")
    return state

def publisher_node(state: SignalState) -> SignalState:
    print("[PublisherAgent] Publishing Markdown using ACP...")
    acp = create_acp_message(
        sender="ConnectorAgent",
        receiver="PublisherAgent",
        task="PublishInsight",
        intent="DeliverFinalInsight",
        payload={
            "summary": state["summary"],
            "tags": state["tags"],
            "insight": state["insight"],
            "source_url": state["article"].get("source_url", "")
        }
    )

    print(f"[ACP] Command: {acp}")
    path = publish_markdown(
        summary=acp["payload"]["summary"],
        tags=acp["payload"]["tags"],
        insight=acp["payload"]["insight"],
        source_url=acp["payload"]["source_url"]
    )
    state["output_path"] = path
    print(f"[PublisherAgent] Output saved to: {path}")
    return state

# --- Graph Definition ---

def build_graph():
    graph = StateGraph(SignalState)

    graph.add_node("scrape", scraper_node)
    graph.add_node("summarize", summarizer_node)
    graph.add_node("tag", tagger_node)
    graph.add_node("connect", connector_node)
    graph.add_node("publish", publisher_node)

    graph.set_entry_point("scrape")
    graph.add_edge("scrape", "summarize")
    graph.add_edge("summarize", "tag")
    graph.add_edge("tag", "connect")
    graph.add_edge("connect", "publish")

    return graph.compile()
