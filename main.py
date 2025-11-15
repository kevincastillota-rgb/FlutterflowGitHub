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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
}


@app.get("/amazon")
def scrape_amazon(url: str = Query(...)):
    try:
        API_KEY = "cb233ab14c5fdb4325499343913b7c63"

        scraper_url = (
            f"https://api.scraperapi.com/?api_key={API_KEY}&amazon=true&url={url}"
        )

        response = requests.get(scraper_url)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        # Título
        titulo = soup.select_one("#productTitle")
        titulo = titulo.get_text(strip=True) if titulo else None

        # Precio
        precio = soup.select_one("#corePrice_feature_div .a-offscreen")
        precio = precio.get_text(strip=True) if precio else None

        # Imagen principal
        imagen = soup.select_one("#landingImage")
        imagen_url = imagen.get("src") if imagen else None

        # Rating
        rating = soup.select_one(".a-icon-alt")
        rating = rating.get_text(strip=True) if rating else None

        # Reviews
        reviews = soup.select_one("#acrCustomerReviewText")
        reviews = reviews.get_text(strip=True) if reviews else None

        return {
            "status": "success",
            "url": url,
            "titulo": titulo,
            "precio": precio,
            "imagen": imagen_url,
            "rating": rating,
            "reviews": reviews
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
