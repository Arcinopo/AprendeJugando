document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('drawingCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let isDrawing = false;
    let currentColor = '#2B2D42';
    let currentSize = 8;
    let editingDrawingId = null;
    let lastCanvasWidth = 0;

    const titleInput = document.getElementById('drawingTitle');
    const saveBtn = document.getElementById('saveDrawingBtn');
    const editingBanner = document.getElementById('editingBanner');
    const editingTitleLabel = document.getElementById('editingTitleLabel');
    const cancelEditBtn = document.getElementById('cancelEditBtn');
    const newDrawingBtn = document.getElementById('newDrawingBtn');
    const feedbackEl = document.getElementById('canvasFeedback');

    function showFeedback(message, type = 'success') {
        if (!feedbackEl) return;
        feedbackEl.className = `alert alert-${type} rounded-4 fw-bold mb-3`;
        feedbackEl.textContent = message;
    }

    function clearCanvasSurface() {
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function resizeCanvas(force = false) {
        const rect = canvas.parentElement.getBoundingClientRect();
        const newWidth = Math.floor(rect.width);
        if (!force && newWidth === lastCanvasWidth) return;

        const savedData = lastCanvasWidth > 0 ? canvas.toDataURL() : null;
        lastCanvasWidth = newWidth;
        canvas.width = newWidth;
        canvas.height = 360;

        clearCanvasSurface();

        if (savedData) {
            const img = new Image();
            img.onload = () => ctx.drawImage(img, 0, 0);
            img.src = savedData;
        }
    }

    resizeCanvas(true);
    window.addEventListener('resize', () => resizeCanvas(false));

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

    // Botón Limpiar Lienzo
    const clearBtn = document.getElementById('clearCanvasBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            clearCanvasSurface();
        });
    }

    // =====================================================================
    // MODO EDICIÓN DE OBRA GUARDADA
    // =====================================================================
    function exitEditMode(clearSurface = false) {
        editingDrawingId = null;
        if (editingBanner) {
            editingBanner.classList.add('d-none');
            editingBanner.classList.remove('d-flex');
        }
        if (newDrawingBtn) newDrawingBtn.classList.add('d-none');
        if (saveBtn) {
            saveBtn.innerHTML = '<i class="bi bi-cloud-arrow-up-fill me-2"></i>Guardar Dibujo';
        }
        if (clearSurface) {
            clearCanvasSurface();
            if (titleInput) titleInput.value = 'Mi Dibujo Libre';
        }
    }

    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', () => exitEditMode(false));
    }

    if (newDrawingBtn) {
        newDrawingBtn.addEventListener('click', () => exitEditMode(true));
    }

    document.querySelectorAll('.edit-drawing-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const drawingId = btn.dataset.id;
            const drawingTitle = btn.dataset.title || 'Mi Obra de Arte';
            const imageUrl = btn.dataset.url;

            const img = new Image();
            img.crossOrigin = 'anonymous';
            img.onload = () => {
                clearCanvasSurface();
                // Ajustar proporcionalmente dentro del lienzo
                const scale = Math.min(canvas.width / img.width, canvas.height / img.height, 1);
                const drawW = img.width * scale;
                const drawH = img.height * scale;
                const offsetX = (canvas.width - drawW) / 2;
                const offsetY = (canvas.height - drawH) / 2;
                ctx.drawImage(img, offsetX, offsetY, drawW, drawH);

                editingDrawingId = drawingId;
                if (titleInput) titleInput.value = drawingTitle;
                if (editingTitleLabel) editingTitleLabel.textContent = drawingTitle;
                if (editingBanner) {
                    editingBanner.classList.remove('d-none');
                    editingBanner.classList.add('d-flex');
                }
                if (newDrawingBtn) newDrawingBtn.classList.remove('d-none');
                if (saveBtn) {
                    saveBtn.innerHTML = '<i class="bi bi-check2-circle me-2"></i>Guardar Cambios';
                }

                canvas.scrollIntoView({ behavior: 'smooth', block: 'center' });
                showFeedback(`Obra "${drawingTitle}" cargada en la pizarra. ¡Continúa dibujando!`, 'info');
            };
            img.onerror = () => {
                showFeedback('No se pudo cargar la imagen para editar. Intenta recargar la página.', 'warning');
            };
            img.src = imageUrl;
        });
    });

    // =====================================================================
    // GUARDAR O ACTUALIZAR DIBUJO EN CLOUDINARY
    // =====================================================================
    if (saveBtn) {
        saveBtn.addEventListener('click', async () => {
            const title = titleInput ? titleInput.value.trim() : 'Mi Obra de Arte';
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const saveUrl = saveBtn.dataset.url;

            saveBtn.disabled = true;
            saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Guardando...';

            try {
                const imageData = canvas.toDataURL('image/png');
                const payload = {
                    image: imageData,
                    title: title,
                    drawing_id: editingDrawingId
                };

                const response = await fetch(saveUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();
                if (result.status === 'ok') {
                    showFeedback(result.message, 'success');
                    window.location.reload();
                } else {
                    showFeedback('Error al guardar: ' + result.message, 'danger');
                }
            } catch (err) {
                showFeedback('Error de conexión al guardar el dibujo.', 'danger');
            } finally {
                saveBtn.disabled = false;
                saveBtn.innerHTML = editingDrawingId
                    ? '<i class="bi bi-check2-circle me-2"></i>Guardar Cambios'
                    : '<i class="bi bi-cloud-arrow-up-fill me-2"></i>Guardar Dibujo';
            }
        });
    }

    // =====================================================================
    // SELECCIONAR Y ELIMINAR DIBUJOS GUARDADOS
    // =====================================================================
    const selectAllCheckbox = document.getElementById('selectAllDrawings');
    const deleteSelectedBtn = document.getElementById('deleteSelectedBtn');
    const selectedCountSpan = document.getElementById('selectedCount');

    function getDrawingCheckboxes() {
        return Array.from(document.querySelectorAll('.drawing-select-checkbox'));
    }

    function updateSelectionState() {
        const checkboxes = getDrawingCheckboxes();
        const checked = checkboxes.filter(cb => cb.checked);

        if (selectedCountSpan) selectedCountSpan.textContent = checked.length;
        if (deleteSelectedBtn) deleteSelectedBtn.disabled = checked.length === 0;
        if (selectAllCheckbox) {
            selectAllCheckbox.checked = checkboxes.length > 0 && checked.length === checkboxes.length;
            selectAllCheckbox.indeterminate = checked.length > 0 && checked.length < checkboxes.length;
        }
    }

    getDrawingCheckboxes().forEach(cb => {
        cb.addEventListener('change', updateSelectionState);
    });

    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', () => {
            const shouldCheck = selectAllCheckbox.checked;
            getDrawingCheckboxes().forEach(cb => {
                cb.checked = shouldCheck;
            });
            updateSelectionState();
        });
    }

    if (deleteSelectedBtn) {
        deleteSelectedBtn.addEventListener('click', async () => {
            const selectedIds = getDrawingCheckboxes()
                .filter(cb => cb.checked)
                .map(cb => cb.value);

            if (selectedIds.length === 0) return;

            const confirmMsg = selectedIds.length === 1
                ? '¿Seguro que quieres borrar este dibujo guardado?'
                : `¿Seguro que quieres borrar los ${selectedIds.length} dibujos seleccionados?`;

            if (!window.confirm(confirmMsg)) return;

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const deleteUrl = deleteSelectedBtn.dataset.url;

            deleteSelectedBtn.disabled = true;

            try {
                const response = await fetch(deleteUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ drawing_ids: selectedIds })
                });

                const result = await response.json();
                if (result.status === 'ok') {
                    selectedIds.forEach(id => {
                        if (String(editingDrawingId) === String(id)) {
                            exitEditMode(true);
                        }
                        const col = document.querySelector(`.drawing-card-col[data-drawing-id="${id}"]`);
                        if (col) col.remove();
                    });
                    updateSelectionState();
                    showFeedback(result.message, 'success');

                    if (getDrawingCheckboxes().length === 0) {
                        window.location.reload();
                    }
                } else {
                    showFeedback(result.message || 'No se pudieron borrar los dibujos.', 'danger');
                    updateSelectionState();
                }
            } catch (err) {
                showFeedback('Error de conexión al eliminar los dibujos.', 'danger');
                updateSelectionState();
            }
        });
    }
});