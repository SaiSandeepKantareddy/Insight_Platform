def basic_tagger(text: str) -> list:
    tags = []
    if "Meta" in text or "Facebook" in text:
        tags.append("Org:Meta")
    if "model" in text:
        tags.append("Topic:Model")
    if "multimodal" in text:
        tags.append("Tech:Multimodal")
    if "open-source" in text:
        tags.append("OpenSource")
    return tags
