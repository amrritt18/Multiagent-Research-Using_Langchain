from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent information.
    Return titles, URLs, and snippets.
    """
    result = tavily.search(query=query, max_results=2)

    out = []

    for r in result["results"]:
        out.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}\n"
        )

    return "\n....\n".join(out)


@tool
def scrap_url(url: str) -> str:
    """Scrape a URL and extract its main readable text.
    Return the page title and article content.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()

        html = response.text

        # Extract the page title
        soup = BeautifulSoup(html, "lxml")
        title = (
            soup.title.get_text(strip=True)
            if soup.title
            else "Title not available"
        )

        # Primary extraction using Trafilatura
        content = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            favor_precision=True
        )

        # Fallback to Readability if extraction fails
        if not content or not content.strip():
            document = Document(html)
            article_html = document.summary()

            article_soup = BeautifulSoup(
                article_html, "lxml"
            )
            content = article_soup.get_text(
                separator="\n",
                strip=True
            )

        if not content or not content.strip():
            return f"Could not extract readable content from: {url}"

        # Normalize excessive whitespace
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r"[ \t]+", " ", content).strip()

        return (
            f"Title: {title}\n"
            f"URL: {url}\n\n"
            f"Content:\n{content[:10000]}"
        )

    except requests.exceptions.Timeout:
        return f"Error: Request timed out while scraping {url}"

    except requests.exceptions.RequestException as e:
        return f"Error: Failed to fetch {url}: {e}"

    except Exception as e:
        return f"Error: Failed to extract content from {url}: {e}"
