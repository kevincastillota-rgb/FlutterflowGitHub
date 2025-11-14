from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Permitir recibir requests desde FlutterFlow
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape")
def scrape(url: str = Query(..., description="URL a scrapear")):
    try:
        # Obtener contenido de la página
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # 🔍 EJEMPLO: obtener el título de la página
        page_title = soup.title.string if soup.title else "No title"

        # 🔍 EJEMPLO: extraer un texto de un div específico
        # div_text = soup.select_one("div.result").get_text(strip=True)

        # 🔍 EJEMPLO: extraer un número, precio, texto, etc
        # precio = soup.find("span", {"class": "price"}).text

        return {
            "status": "success",
            "url": url,
            "title": page_title,
            # "resultado": div_text,
            # "precio": precio
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
