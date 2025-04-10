import asyncio
import httpx
import aiofiles
from selectolax.parser import HTMLParser
from urllib.parse import urljoin, urlparse, parse_qs, unquote
import tempfile
import logging
import os
from typing import List
from PyPDF2 import PdfReader

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

SEARCH_ENGINES = {
    "Google": "https://www.google.com/search",
}

KEYWORDS = [
    "radio frequency analysis", "embedded systems", "IoT devices",
    "cybersecurity", "security", "ethical hacking", "hacking"
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

QUERY = (
    "filetype:pdf site:.gov OR site:.mil OR site:.edu OR site:.com "
    + "(".join(KEYWORDS) + ")"
)


def parse_pdf_url_from_google(href: str) -> str | None:
    """Parses a raw Google search result href to extract a clean PDF URL."""
    if "/url?q=" not in href:
        return None
    url_part = unquote(href.split("/url?q=")[-1].split("&")[0])
    if url_part.endswith(".pdf") and any(domain in url_part for domain in [".gov", ".mil", ".edu", ".com"]):
        return url_part
    return None


async def fetch_search_results(engine_url: str, query: str) -> List[str]:
    """Fetches PDF URLs from the search engine results page."""
    pdf_links = []
    async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
        params = {"q": query, "num": 100}
        try:
            resp = await client.get(engine_url, params=params)
            resp.raise_for_status()
            html = HTMLParser(resp.text)

            for link in html.css("a"):
                href = link.attributes.get("href")
                if href:
                    clean_url = parse_pdf_url_from_google(href)
                    if clean_url:
                        pdf_links.append(clean_url)
        except Exception as e:
            logging.error(f"Failed to fetch search results: {e}")
    return pdf_links


async def download_and_process_pdf(url: str, output_dir: str):
    """Downloads and extracts the first page text of a PDF."""
    filename = os.path.basename(urlparse(url).path)
    filepath = os.path.join(output_dir, filename)

    async with httpx.AsyncClient(headers=HEADERS, timeout=30) as client:
        try:
            resp = await client.get(url, follow_redirects=True)
            resp.raise_for_status()

            if "application/pdf" not in resp.headers.get("Content-Type", "").lower():
                logging.warning(f"Skipping non-PDF content from: {url}")
                return

            async with aiofiles.open(filepath, mode="wb") as f:
                await f.write(resp.content)

            reader = PdfReader(filepath)
            num_pages = len(reader.pages)
            logging.info(f"Downloaded {filename} with {num_pages} pages")

            first_page = reader.pages[0]
            text = first_page.extract_text() or ""
            logging.info(f"First 200 characters of {filename}:\n{text[:200]}")

        except Exception as e:
            logging.error(f"Error downloading or parsing PDF {url}: {e}")
            if os.path.exists(filepath):
                os.remove(filepath)


async def main():
    output_dir = "rf_files"
    os.makedirs(output_dir, exist_ok=True)

    all_pdf_urls = []
    for name, url in SEARCH_ENGINES.items():
        logging.info(f"Searching using {name}...")
        results = await fetch_search_results(url, QUERY)
        all_pdf_urls.extend(results)
        logging.info(f"Found {len(results)} results from {name}")

    unique_urls = list(set(all_pdf_urls))
    logging.info(f"Total unique PDF URLs: {len(unique_urls)}")

    await asyncio.gather(*(download_and_process_pdf(url, output_dir) for url in unique_urls))


if __name__ == "__main__":
    asyncio.run(main())
