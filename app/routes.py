from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.model import Model
from PIL import Image
import numpy as np

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
model = Model()
model.cargar("hibrido.keras")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
    })

@router.post("/detectar", response_class=JSONResponse)
async def detectar(request: Request):
    form = await request.form()
    file = form.get("file")
    if not file:
        return JSONResponse({"error": "No file uploaded"}, status_code=400)
    
    try:
        image = Image.open(file.file)
        
        # ✅ DETECTAR si es escala de grises o RGB
        if image.mode in ['L', 'LA', 'P', '1']:
            # Es escala de grises - convertir a RGB
            image = image.convert('RGB')
        elif image.mode == 'RGBA':
            # Es RGBA (con transparencia) - quitar canal alpha
            image = image.convert('RGB')
        else:
            # Ya es RGB
            pass
        
        # Redimensionar y preprocesar
        image = image.resize((224, 224))
        image_array = np.array(image)
        
        # Añadir dimensión de batch
        image_array = np.expand_dims(image_array, axis=0)
        
        # Predecir
        probability_prediction = model.predecir(image_array)
        
        # Interpretar resultado
        result = "Neumonía detectada" if probability_prediction > 0.5 else "No se detecta neumonía"
        return JSONResponse({"data" : {
            "result": result, "confidence": round(
                float(probability_prediction if probability_prediction > 0.5 else 1 - probability_prediction) * 100, 2
            )
        }})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)