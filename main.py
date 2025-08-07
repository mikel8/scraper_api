from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape")
async def scrape_profile(data: ScrapeRequest):
    try:
        url = data.url
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Very simple Twitter scraper (you'd improve this)
        title = soup.find("title").text
        return {"title": title}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
