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

@app.get("/bestbuy-scrape")
def bestbuy_scrape(url: str = Query(...)):
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

        soup = BeautifulSoup(html, "html.parser")

        # ----------- BEST BUY SELECTORS -----------

        # TITULO
        titulo = None
        titulo_el = soup.select_one(".sku-title h1")
        if titulo_el:
            titulo = titulo_el.get_text(strip=True)

        # PRECIO
        precio = None
        precio_el = soup.select_one(".priceView-hero-price.priceView-customer-price span")
        if precio_el:
            precio = precio_el.get_text(strip=True)

        # IMAGEN PRINCIPAL
        imagen = None
        imagen_el = soup.select_one("img.primary-image")
        if imagen_el and imagen_el.get("src"):
            imagen = imagen_el["src"]

        # RATING
        rating = None
        rating_el = soup.select_one(".ugc-c-review-average")
        if rating_el:
            rating = rating_el.get_text(strip=True)

        return {
            "status": "success",
            "url": url,
            "titulo": titulo,
            "precio": precio,
            "imagen": imagen,
            "rating": rating
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
