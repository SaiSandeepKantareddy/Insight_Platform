
import trafilatura

def scrape_article(url: str) -> dict:
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)

    return {
        "title": url.split("/")[-1].replace("-", " ").capitalize(),
        "text": text if text else "",
        "source_url": url
    }
