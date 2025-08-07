from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

API_KEY = "your_secret_api_key"

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape")
async def scrape_profile(data: ScrapeRequest, x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        url = data.url
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Referer": "https://x.com/",
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        title_tag = soup.find("title")

        if not title_tag or not title_tag.text:
            raise HTTPException(status_code=404, detail="Title tag not found")

        return {
            "title": title_tag.text.strip(),
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Request error: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")
