from keras.applications.efficientnet import preprocess_input as pre_efficientnetb0
from keras.applications.densenet import preprocess_input as pre_densenet121
from keras import models
import keras, logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        force=True  # 🔥 fuerza la reconfiguración
    )

@keras.saving.register_keras_serializable()
def preprocess_effnet(x):
    return pre_efficientnetb0(x)

@keras.saving.register_keras_serializable()
def preprocess_densenet(x):
    return pre_densenet121(x)

class Model:
    def __init__(self):
        self.__modelo: models.Model | None = None
    
    def cargar(self, ruta_guardado):
        configure_logging()
        logger = logging.getLogger(__name__)
        logger.info("Cargando modelo...")
        self.__modelo = models.load_model(ruta_guardado)
        logger.info(f"✅ Modelo cargado desde: {ruta_guardado}")

    def predecir(self, imagen_array):
        prediccion = self.__modelo.predict(imagen_array)
        return prediccion[0][0]