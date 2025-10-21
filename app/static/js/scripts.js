const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const btnPredecir = document.getElementById("btn-predecir");
const imageContainer = document.getElementById("imageContainer");
const resultadoInput = document.getElementById("resultado");
const probabilidadInput = document.getElementById("probabilidad");
const modal = new bootstrap.Modal(document.getElementById('cnnNeumoniaModal'), {
    keyboard: false,
    backdrop: 'static',
    focus: false
});

// FUNCIÓN DE CIERRE FORZADO - ESTA SÍ FUNCIONA
function forceCloseModal() {
    console.log('🔴 Forzando cierre del modal...');
    
    const modalElement = document.getElementById('cnnNeumoniaModal');
    if (!modalElement) return;
    
    // 1. Remover completamente las clases de Bootstrap
    modalElement.classList.remove('show', 'fade');
    modalElement.style.display = 'none';
    modalElement.setAttribute('aria-hidden', 'true');
    
    // 2. Eliminar TODOS los backdrops (puede haber múltiples)
    const backdrops = document.querySelectorAll('.modal-backdrop');
    backdrops.forEach(backdrop => {
        backdrop.remove();
    });
    
    // 3. Restaurar el body completamente
    document.body.classList.remove('modal-open');
    document.body.style.overflow = 'auto';
    document.body.style.paddingRight = '';
    
    // 4. Destruir cualquier instancia de Bootstrap
    const existingModal = bootstrap.Modal.getInstance(modalElement);
    if (existingModal) {
        try {
            existingModal.dispose();
        } catch (e) {
            console.log('No se pudo destruir instancia:', e);
        }
    }
    
    console.log('✅ Modal cerrado forzosamente');
}

// FUNCIÓN PARA MOSTRAR MODAL (también con reinicio)
function forceShowModal() {
    console.log('🟢 Forzando apertura del modal...');
    
    // Primero cerrar cualquier modal abierto
    forceCloseModal();
    
    const modalElement = document.getElementById('cnnNeumoniaModal');
    if (!modalElement) return;
    
    // Mostrar manualmente
    modalElement.style.display = 'block';
    modalElement.classList.add('show');
    modalElement.removeAttribute('aria-hidden');
    modalElement.setAttribute('aria-hidden', 'false');
    
    // Crear backdrop manualmente
    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop fade show';
    document.body.appendChild(backdrop);
    
    // Estilos del body
    document.body.classList.add('modal-open');
    document.body.style.overflow = 'hidden';
    
    console.log('✅ Modal abierto forzosamente');
}

//uploadArea.addEventListener("click", () => fileInput.click());

uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("dragover");
});
uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("dragover");
});
uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    handleFile(file);
});
btnPredecir.addEventListener("click", sendImage);

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    handleFile(file);
});

function handleFile(file) {
    resultadoInput.value = "";
    probabilidadInput.value = "";

    if (file && (file.type === "image/png" || file.type === "image/jpeg")) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imageContainer.innerHTML = `<img src="${e.target.result}" alt="Vista previa">`;
        };
        reader.readAsDataURL(file);
    } else {
        imageContainer.innerHTML = `<p class="placeholder">Formato no válido. Solo PNG o JPG.</p>`;
    }
}

function sendImage() {
    const img = imageContainer.querySelector("img");
    
    if (!img) {
        alert("Por favor, sube una imagen primero.");
        return;
    }

    forceShowModal();

    const formData = new FormData();
    const file = fileInput.files[0];
    formData.append("file", file);

    fetch('/detectar', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
            resultadoInput.value = data.data.result;
            probabilidadInput.value = data.data.confidence + "%";
      })
      .catch((error) => {
            console.log('Intentando ocultar modal...');
      })
      .finally(() => {
            console.log('Intentando ocultar modal en finally...');
            forceCloseModal();
      });
}