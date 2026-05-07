import requests
WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary"
def search_wikipedia(query: str) -> dict:
    """
    Returns {"extract": ..., "url": ...} or {"extract": None, "url": None}
    """
    #clean query for URL
    topic = query.strip().replace(" ", "_")
    try:
        res = requests.get(f"{WIKI_API}/{topic}", timeout=5)
        if res.status_code == 200:
            data = res.json()
            return {
                "extract": data.get("extract"),
                "url": data.get("content_urls", {})
                           .get("desktop", {})
                           .get("page")
            }
    except Exception:
        pass
    return {"extract": None, "url": None}        
    