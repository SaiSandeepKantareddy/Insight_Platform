# Model Context Protocol (MCP)

from datetime import datetime

def create_mcp_payload(goal, context, input_text, format_type="markdown"):
    return {
        "goal": goal,
        "context": context,
        "input": input_text,
        "format": format_type,
        "timestamp": str(datetime.now())
    }
