from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRAPINGBEE_API_KEY = "PH1E7FL1MKIF1U0QIQ911W6XSCD1KFEM839JMH2ZY7D7T8OPQFQHVJKC9DX7INEGON369V75FBVPO2JF"

@app.get("/scrapingbee")
def scrapingbee(url: str = Query(...)):
    try:
        bee_url = (
            f"https://app.scrapingbee.com/api/v1/"
            f"?api_key={SCRAPINGBEE_API_KEY}"
            f"&render_js=true"
            f"&url={url}"
        )

        response = requests.get(bee_url)
        response.raise_for_status()
        html = response.text

        # Convertimos el HTML a un objeto BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # EJEMPLO: extraer título genérico
        title = soup.title.string if soup.title else "(Sin título)"

        return {
            "status": "success",
            "url": url,
            "title": title,
            "html_length": len(html)  # para verificar que sí aparece el HTML real
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
