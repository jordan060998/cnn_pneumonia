from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        force=True  # 🔥 fuerza la reconfiguración
    )

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Detección de neumonía en radiografías de tórax mediante Red Neuronal Convolucional",
    description="API para detectar neumonía en radiografías de tórax utilizando una Red Neuronal Convolucional (CNN).",
    version="1.0.0",
    contact={
        "name": "Jordan García Blas",
        "email": "jgarciablas98@gmail.com",
        "university": "Universidad Nacional de Trujillo",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)
logger.info("✅ App factory inicializada")