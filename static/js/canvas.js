document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('drawingCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let isDrawing = false;
    let currentColor = '#2B2D42';
    let currentSize = 6;

    // Ajustar tamaño interno del canvas al contenedor responsivo
    function resizeCanvas() {
        const rect = canvas.parentElement.getBoundingClientRect();
        const savedData = canvas.toDataURL();
        canvas.width = rect.width;
        canvas.height = 360;

        // Fondo blanco sólido (evita fondos negros al exportar PNG/JPEG)
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const img = new Image();
        img.onload = () => ctx.drawImage(img, 0, 0);
        img.src = savedData;
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    function getCoordinates(e) {
        const rect = canvas.getBoundingClientRect();
        if (e.touches && e.touches.length > 0) {
            return {
                x: e.touches[0].clientX - rect.left,
                y: e.touches[0].clientY - rect.top
            };
        }
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }

    function startDraw(e) {
        if (e.cancelable) e.preventDefault();
        isDrawing = true;
        const pos = getCoordinates(e);
        ctx.beginPath();
        ctx.moveTo(pos.x, pos.y);
    }

    function draw(e) {
        if (!isDrawing) return;
        if (e.cancelable) e.preventDefault();
        const pos = getCoordinates(e);

        ctx.lineWidth = currentSize;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.strokeStyle = currentColor;

        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
    }

    function stopDraw() {
        if (!isDrawing) return;
        isDrawing = false;
        ctx.closePath();
    }

    // Eventos Ratón (PC)
    canvas.addEventListener('mousedown', startDraw);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDraw);
    canvas.addEventListener('mouseleave', stopDraw);

    // Eventos Táctiles (Móvil / Tablet)
    canvas.addEventListener('touchstart', startDraw, { passive: false });
    canvas.addEventListener('touchmove', draw, { passive: false });
    canvas.addEventListener('touchend', stopDraw);

    // Selector de Colores
    document.querySelectorAll('.color-swatch').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.color-swatch').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentColor = btn.dataset.color;
        });
    });

    // Selector de Grosor de Pincel
    document.querySelectorAll('.brush-size').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.brush-size').forEach(b => b.classList.remove('btn-dark'));
            btn.classList.add('btn-dark');
            currentSize = parseInt(btn.dataset.size, 10);
        });
    });

    // Botón Borrar Todo
    const clearBtn = document.getElementById('clearCanvasBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            ctx.fillStyle = '#FFFFFF';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        });
    }

    // Botón Guardar Dibujo en Cloudinary
    const saveBtn = document.getElementById('saveDrawingBtn');
    if (saveBtn) {
        saveBtn.addEventListener('click', async () => {
            const titleInput = document.getElementById('drawingTitle');
            const title = titleInput ? titleInput.value.trim() : 'Mi Obra de Arte';
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const saveUrl = saveBtn.dataset.url;

            saveBtn.disabled = true;
            saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Guardando...';

            try {
                const imageData = canvas.toDataURL('image/png');
                const response = await fetch(saveUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ image: imageData, title: title })
                });

                const result = await response.json();
                if (result.status === 'ok') {
                    alert(result.message);
                    window.location.reload();
                } else {
                    alert('Error al guardar: ' + result.message);
                }
            } catch (err) {
                alert('Error de conexión al guardar el dibujo.');
            } finally {
                saveBtn.disabled = false;
                saveBtn.innerHTML = 'Guardar Dibujo';
            }
        });
    }
});