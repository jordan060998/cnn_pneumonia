import onnxruntime as ort
import onnx  # Opcional para chequeo

class Model:
    def __init__(self):
        self.session = None
    
    def cargar(self, model_path: str):
        self.onnx_model = onnx.load(model_path)
        onnx.checker.check_model(self.onnx_model)
        # Crear sesión (usa 'CPUExecutionProvider' o 'CUDAExecutionProvider')
        # Configurar providers (CPU por default, GPU si disponible)
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        self.session = ort.InferenceSession(model_path, providers=providers)
    
    def predecir(self, imagen_array):
        input_name = self.session.get_inputs()[0].name
        return self.session.run(None, {input_name: imagen_array})[0]
