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


@app.get("/bestbuy")
def bestbuy(url: str = Query(...)):
    try:
        # Extraer SKU desde la URL
        sku = url.rstrip("/").split("/")[-1]

        # API interna de BestBuy
        api_url = f"https://www.bestbuy.com/api/3.0/clickstream/products/{sku}?sku={sku}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        product = data.get("product", {})

        return {
            "status": "success",
            "sku": sku,
            "titulo": product.get("names", {}).get("title"),
            "precio": product.get("pricing", {}).get("regularPrice"),
            "precio_oferta": product.get("pricing", {}).get("currentPrice"),
            "imagen": product.get("images", {}).get("standard"),
            "rating": product.get("customerReviews", {}).get("averageScore"),
            "reviews": product.get("customerReviews", {}).get("count"),
            "descripcion": product.get("descriptions", {}).get("short"),
            "en_stock": product.get("availability", {}).get("displayValue"),
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
