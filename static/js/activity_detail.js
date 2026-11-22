document.addEventListener('DOMContentLoaded', () => {
    const workspace = document.getElementById('activityWorkspace');
    if (!workspace) return;

    const ACTIVITY_TYPE = workspace.dataset.activityType || '';
    const CHECK_URL = workspace.dataset.checkUrl || '';
    const DEFAULT_QUESTION = workspace.dataset.defaultQuestion || '';
    const extraScript = document.getElementById('activity-extra-data');
    const EXTRA_DATA = extraScript ? JSON.parse(extraScript.textContent || '{}') : {};

    async function postVerification(payload) {
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        const csrfToken = csrfInput ? csrfInput.value : '';
        const feedbackBox = document.getElementById('feedbackBox');
        const nextWrapper = document.getElementById('nextBtnWrapper');

        const response = await fetch(CHECK_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (feedbackBox) {
            feedbackBox.classList.remove('d-none');
            if (data.correct) {
                let extraExplanation = '';
                if (data.explanation) {
                    extraExplanation = `<div class="mt-2 pt-2 border-top border-success fs-6 fw-normal text-dark"><i class="bi bi-lightbulb-fill text-warning me-1"></i><strong>Explicación científica:</strong> ${data.explanation}</div>`;
                }
                feedbackBox.innerHTML = `<div class="alert alert-success rounded-4 fs-4 fw-bold text-start"><i class="bi bi-star-fill me-2"></i>${data.message}${extraExplanation}</div>`;
                if (nextWrapper) nextWrapper.classList.remove('d-none');
            } else {
                feedbackBox.innerHTML = `<div class="alert alert-warning rounded-4 fs-5 fw-bold"><i class="bi bi-exclamation-circle-fill me-2"></i>${data.message}</div>`;
            }
        }
        return data;
    }

    // Botones de opción múltiple y dibujo completado
    document.querySelectorAll('.js-submit-answer').forEach(btn => {
        btn.addEventListener('click', () => {
            postVerification({ answer: btn.dataset.answer || '' });
        });
    });

    // =========================================================================
    // 1. CAZADORES DE ERRORES
    // =========================================================================
    const hunterCorrections = {};

    function initErrorHunter() {
        const segments = EXTRA_DATA.segments || [];
        const container = document.getElementById('hunterTextContainer');
        const counter = document.getElementById('hunterCounter');
        const submitBtn = document.getElementById('btnSubmitErrorHunter');
        if (!container) return;

        const totalErrors = segments.filter(s => s.is_error).length;
        if (counter) counter.textContent = `Errores corregidos: 0 / ${totalErrors}`;
        container.innerHTML = '';

        segments.forEach((seg, idx) => {
            const span = document.createElement('span');
            span.className = 'error-token';
            span.dataset.index = idx;
            span.textContent = hunterCorrections[idx] || seg.text;

            span.addEventListener('click', () => handleTokenClick(idx, seg, span));
            container.appendChild(span);
        });

        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                postVerification({ corrections: hunterCorrections });
            });
        }
    }

    function handleTokenClick(idx, seg, spanEl) {
        const toast = document.getElementById('hunterToast');
        const box = document.getElementById('hunterCorrectionBox');

        if (!seg.is_error) {
            spanEl.classList.add('token-ok-flash');
            if (toast) toast.textContent = 'Esa parte está bien escrita. Sigue buscando el error en el texto.';
            setTimeout(() => spanEl.classList.remove('token-ok-flash'), 600);
            return;
        }

        document.querySelectorAll('.error-token').forEach(el => el.classList.remove('token-selected'));
        spanEl.classList.add('token-selected');

        if (toast) toast.textContent = '';
        if (box) box.classList.remove('d-none');

        const hintEl = document.getElementById('hunterHintText');
        if (hintEl) {
            hintEl.innerHTML = `<i class="bi bi-lightbulb-fill text-warning me-1"></i> Pista: ${seg.reason || 'Elige la forma correcta'} ("${seg.text}")`;
        }

        const optsContainer = document.getElementById('hunterOptionsContainer');
        if (!optsContainer) return;
        optsContainer.innerHTML = '';

        (seg.options || []).forEach(opt => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-outline-dark rounded-pill fw-bold px-3 py-2';
            btn.textContent = opt;
            btn.addEventListener('click', () => {
                hunterCorrections[idx] = opt;
                spanEl.textContent = opt;
                spanEl.classList.remove('token-selected');
                spanEl.classList.add('token-fixed');
                if (box) box.classList.add('d-none');

                const segments = EXTRA_DATA.segments || [];
                const totalErrors = segments.filter(s => s.is_error).length;
                const fixedCount = Object.keys(hunterCorrections).length;
                const counter = document.getElementById('hunterCounter');
                if (counter) counter.textContent = `Errores corregidos: ${fixedCount} / ${totalErrors}`;
            });
            optsContainer.appendChild(btn);
        });
    }

    // =========================================================================
    // 2. COMPLETAR EL CÓMIC
    // =========================================================================
    function initComicFill() {
        const panels = EXTRA_DATA.panels || [];
        const container = document.getElementById('comicPanelsContainer');
        const submitBtn = document.getElementById('btnSubmitComicFill');
        if (!container) return;

        container.innerHTML = '';
        const colClass = panels.length <= 2 ? 'col-12 col-md-6' : 'col-12 col-md-4';

        panels.forEach((panel, idx) => {
            const col = document.createElement('div');
            col.className = colClass;

            const bg = panel.scene_bg || '#EFF6FF';
            const isThought = panel.bubble_type === 'thought';
            const bubbleClass = isThought ? 'thought-bubble' : 'speech-bubble';

            let bubbleContent = '';
            if (panel.readonly) {
                bubbleContent = `<p class="mb-0 fw-bold text-dark">${panel.starter_text || ''}</p>`;
            } else {
                bubbleContent = `
                    <textarea class="form-control border-0 bg-transparent fw-bold text-dark comic-input p-0"
                              rows="3"
                              data-panel-index="${idx}"
                              placeholder="${panel.placeholder || 'Escribe aquí el diálogo...'}">${panel.starter_text || ''}</textarea>
                `;
            }

            col.innerHTML = `
                <div class="comic-panel h-100 d-flex flex-column justify-content-between p-3" style="background-color: ${bg};">
                    <div>
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge bg-dark rounded-pill">Viñeta ${idx + 1}</span>
                            <span class="small fw-bold text-secondary">${panel.character_name || ''}</span>
                        </div>
                        ${panel.narration ? `<div class="comic-narration mb-2">${panel.narration}</div>` : ''}
                        <div class="${bubbleClass} mb-3">
                            ${bubbleContent}
                        </div>
                    </div>
                    <div class="text-center mt-2">
                        <img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/${panel.character_icon || '1f600'}.svg"
                             alt="${panel.character_name || 'Personaje'}" width="76" height="76">
                    </div>
                </div>
            `;
            container.appendChild(col);
        });

        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                const dialogues = panels.map((panel, idx) => {
                    if (panel.readonly) return panel.starter_text || '';
                    const input = document.querySelector(`.comic-input[data-panel-index="${idx}"]`);
                    return input ? input.value.trim() : '';
                });
                postVerification({ dialogues: dialogues });
            });
        }
    }

    // =========================================================================
    // 3. SOPA DE LETRAS Y CRUCIGRAMA TEMÁTICO
    // =========================================================================
    let soupStartCell = null;
    const foundWordsSet = new Set();

    function initWordGame() {
        const wrapper = document.getElementById('wordGameWrapper');
        if (!wrapper) return;

        const mode = EXTRA_DATA.mode || 'soup';
        if (mode === 'crossword') {
            renderCrossword(wrapper);
        } else {
            renderWordSoup(wrapper);
        }
    }

    function renderWordSoup(wrapper) {
        const grid = EXTRA_DATA.grid || [];
        const words = EXTRA_DATA.words || [];
        const themeName = EXTRA_DATA.theme_name || 'Vocabulario';

        wrapper.innerHTML = `
            <div class="mb-3">
                <span class="badge bg-info text-dark rounded-pill fs-6 px-3 py-2">
                    Tema: ${themeName}
                </span>
                <p class="small text-muted mt-2 mb-0">
                    Toca la <strong>primera letra</strong> y luego la <strong>última letra</strong> de cada palabra escondida.
                </p>
            </div>
            <div class="row g-4 align-items-center justify-content-center">
                <div class="col-12 col-md-7 d-flex justify-content-center">
                    <div id="soupGrid" class="word-grid"></div>
                </div>
                <div class="col-12 col-md-5 text-start">
                    <div class="bg-light rounded-4 p-3 border">
                        <h2 class="h5 fw-bold mb-3"><i class="bi bi-list-check text-success me-1"></i> Palabras a encontrar</h2>
                        <div id="soupWordList" class="d-flex flex-column gap-2"></div>
                    </div>
                </div>
            </div>
        `;

        const gridEl = document.getElementById('soupGrid');
        gridEl.style.gridTemplateColumns = `repeat(${grid[0]?.length || 8}, 1fr)`;

        grid.forEach((row, r) => {
            row.forEach((letter, c) => {
                const cell = document.createElement('button');
                cell.type = 'button';
                cell.className = 'word-cell';
                cell.textContent = letter;
                cell.dataset.r = r;
                cell.dataset.c = c;
                cell.addEventListener('click', () => handleSoupCellClick(r, c));
                gridEl.appendChild(cell);
            });
        });

        const listEl = document.getElementById('soupWordList');
        words.forEach(item => {
            const w = item.word.toUpperCase();
            const badge = document.createElement('div');
            badge.id = `word-item-${w}`;
            badge.className = 'd-flex align-items-center justify-content-between p-2 rounded-3 bg-white border';
            badge.innerHTML = `
                <div class="d-flex align-items-center gap-2">
                    ${item.icon ? `<img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/${item.icon}.svg" width="26" height="26" alt="${w}">` : ''}
                    <div>
                        <span class="fw-bold d-block">${w}</span>
                        ${item.clue ? `<small class="text-muted">${item.clue}</small>` : ''}
                    </div>
                </div>
                <span class="badge bg-secondary rounded-pill status-pill">Buscar</span>
            `;
            listEl.appendChild(badge);
        });
    }

    function handleSoupCellClick(r, c) {
        document.querySelectorAll('.word-cell').forEach(el => el.classList.remove('cell-selected'));

        if (!soupStartCell) {
            soupStartCell = { r, c };
            const el = document.querySelector(`.word-cell[data-r="${r}"][data-c="${c}"]`);
            if (el) el.classList.add('cell-selected');
            return;
        }

        const start = soupStartCell;
        soupStartCell = null;

        const dr = r - start.r;
        const dc = c - start.c;
        const steps = Math.max(Math.abs(dr), Math.abs(dc));

        if (steps === 0 || (dr !== 0 && dc !== 0 && Math.abs(dr) !== Math.abs(dc))) {
            return;
        }

        const stepR = dr === 0 ? 0 : dr / steps;
        const stepC = dc === 0 ? 0 : dc / steps;
        const grid = EXTRA_DATA.grid || [];
        const coords = [];
        let letters = '';

        for (let i = 0; i <= steps; i++) {
            const curR = start.r + i * stepR;
            const curC = start.c + i * stepC;
            coords.push({ r: curR, c: curC });
            letters += grid[curR][curC];
        }

        const reversed = letters.split('').reverse().join('');
        const targetWords = (EXTRA_DATA.words || []).map(w => w.word.toUpperCase());
        const matched = targetWords.find(w => w === letters || w === reversed);

        if (matched && !foundWordsSet.has(matched)) {
            foundWordsSet.add(matched);
            coords.forEach(({ r: cr, c: cc }) => {
                const cellEl = document.querySelector(`.word-cell[data-r="${cr}"][data-c="${cc}"]`);
                if (cellEl) cellEl.classList.add('cell-found');
            });

            const itemEl = document.getElementById(`word-item-${matched}`);
            if (itemEl) {
                itemEl.classList.add('border-success', 'bg-success', 'bg-opacity-10');
                const pill = itemEl.querySelector('.status-pill');
                if (pill) {
                    pill.className = 'badge bg-success rounded-pill status-pill';
                    pill.innerHTML = '<i class="bi bi-check-lg"></i>';
                }
            }

            if (foundWordsSet.size === targetWords.length) {
                postVerification({ found_words: Array.from(foundWordsSet) });
            }
        }
    }

    function renderCrossword(wrapper) {
        const solutionGrid = EXTRA_DATA.solution_grid || [];
        const cellNumbers = EXTRA_DATA.cell_numbers || {};
        const clues = EXTRA_DATA.clues || { across: [], down: [] };
        const themeName = EXTRA_DATA.theme_name || 'Crucigrama';

        wrapper.innerHTML = `
            <div class="mb-3">
                <span class="badge bg-primary rounded-pill fs-6 px-3 py-2">Tema: ${themeName}</span>
            </div>
            <div class="row g-4 align-items-start justify-content-center">
                <div class="col-12 col-md-6 d-flex justify-content-center">
                    <div id="cwGrid" class="cw-grid"></div>
                </div>
                <div class="col-12 col-md-6 text-start">
                    <div class="bg-light rounded-4 p-3 border mb-3">
                        <h2 class="h6 fw-bold text-primary mb-2"><i class="bi bi-arrow-right-circle-fill me-1"></i> Horizontales</h2>
                        <ul class="list-unstyled mb-3 small">
                            ${(clues.across || []).map(c => `<li class="mb-1"><strong>${c.num}.</strong> ${c.clue}</li>`).join('')}
                        </ul>
                        <h2 class="h6 fw-bold text-success mb-2"><i class="bi bi-arrow-down-circle-fill me-1"></i> Verticales</h2>
                        <ul class="list-unstyled mb-0 small">
                            ${(clues.down || []).map(c => `<li class="mb-1"><strong>${c.num}.</strong> ${c.clue}</li>`).join('')}
                        </ul>
                    </div>
                    <button type="button" id="btnSubmitCrossword" class="btn btn-primary btn-lg btn-kid w-100 fs-5">
                        <i class="bi bi-check2-square me-2"></i>Comprobar Crucigrama
                    </button>
                </div>
            </div>
        `;

        const cwGrid = document.getElementById('cwGrid');
        const cols = solutionGrid[0]?.length || 7;
        cwGrid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;

        solutionGrid.forEach((row, r) => {
            row.forEach((char, c) => {
                const box = document.createElement('div');
                if (!char) {
                    box.className = 'cw-cell cw-block';
                } else {
                    box.className = 'cw-cell cw-active';
                    const num = cellNumbers[`${r},${c}`];
                    box.innerHTML = `
                        ${num ? `<span class="cw-num">${num}</span>` : ''}
                        <input type="text" maxlength="1" class="cw-input" data-key="${r},${c}" aria-label="Fila ${r + 1} Columna ${c + 1}">
                    `;
                }
                cwGrid.appendChild(box);
            });
        });

        cwGrid.querySelectorAll('.cw-input').forEach((input, idx, allInputs) => {
            input.addEventListener('input', () => {
                input.value = input.value.toUpperCase().replace(/[^A-ZÑÁÉÍÓÚ]/g, '');
                if (input.value && allInputs[idx + 1]) {
                    allInputs[idx + 1].focus();
                }
            });
        });

        const submitCwBtn = document.getElementById('btnSubmitCrossword');
        if (submitCwBtn) {
            submitCwBtn.addEventListener('click', () => {
                const gridAnswers = {};
                document.querySelectorAll('.cw-input').forEach(inp => {
                    gridAnswers[inp.dataset.key] = inp.value.trim().toUpperCase();
                });
                postVerification({ grid_answers: gridAnswers });
            });
        }
    }

    // =========================================================================
    // 4. LABERINTO NUMÉRICO EN PLANO CARTESIANO (X, Y)
    // =========================================================================
    let mazePath = [];

    function initMathMaze() {
        const gridEl = document.getElementById('mathMazeGrid');
        if (!gridEl) return;

        const start = EXTRA_DATA.start || [0, 0];
        mazePath = [[start[0], start[1]]];
        renderMathMaze();

        const resetBtn = document.getElementById('resetMazeBtn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                mazePath = [[start[0], start[1]]];
                const feedbackBox = document.getElementById('feedbackBox');
                if (feedbackBox) feedbackBox.classList.add('d-none');

                const helper = document.getElementById('mazeHelperText');
                if (helper) {
                    helper.className = 'small text-dark fw-semibold mb-0';
                    helper.textContent = 'Muévete en el plano (X, Y) tocando la casilla vecina con el resultado correcto hasta llegar a la meta.';
                }
                renderMathMaze();
            });
        }
    }

    function renderMathMaze() {
        const grid = EXTRA_DATA.grid || [];
        const steps = EXTRA_DATA.steps || [];
        const rowsCount = grid.length || 4;
        const colsCount = grid[0]?.length || 4;
        const goal = EXTRA_DATA.goal || [rowsCount - 1, colsCount - 1];
        const start = EXTRA_DATA.start || [0, 0];

        const gridEl = document.getElementById('mathMazeGrid');
        const stepLabel = document.getElementById('mazeStepLabel');
        const coordBadge = document.getElementById('mazeCoordBadge');
        const opBox = document.getElementById('mazeOperationBox');
        const xAxisEl = document.getElementById('mazeXAxis');
        const yAxisEl = document.getElementById('mazeYAxis');
        const svgEl = document.getElementById('mazeTrailSvg');

        const currentStepIdx = mazePath.length - 1;
        const [curR, curC] = mazePath[currentStepIdx];

        if (coordBadge) {
            coordBadge.textContent = `Posición: (X=${curC + 1}, Y=${curR + 1})`;
        }

        if (currentStepIdx < steps.length) {
            if (stepLabel) stepLabel.textContent = `Paso ${currentStepIdx + 1} de ${steps.length}`;
            if (opBox) opBox.textContent = `${steps[currentStepIdx].expression} = ?`;
        } else {
            if (stepLabel) stepLabel.textContent = 'Meta alcanzada';
            if (opBox) opBox.textContent = '¡Laberinto completado!';
        }

        if (xAxisEl) {
            xAxisEl.style.gridTemplateColumns = `repeat(${colsCount}, 1fr)`;
            xAxisEl.innerHTML = Array.from({ length: colsCount }, (_, i) =>
                `<span class="maze-axis-pill">X${i + 1}</span>`
            ).join('');
        }

        if (yAxisEl) {
            yAxisEl.style.gridTemplateRows = `repeat(${rowsCount}, 1fr)`;
            yAxisEl.innerHTML = Array.from({ length: rowsCount }, (_, i) =>
                `<span class="maze-axis-pill">Y${i + 1}</span>`
            ).join('');
        }

        if (svgEl) {
            const vbW = colsCount * 100;
            const vbH = rowsCount * 100;
            svgEl.setAttribute('viewBox', `0 0 ${vbW} ${vbH}`);

            if (mazePath.length > 1) {
                const pts = mazePath.map(([pr, pc]) => `${pc * 100 + 50},${pr * 100 + 50}`).join(' ');
                const circles = mazePath.map(([pr, pc]) =>
                    `<circle cx="${pc * 100 + 50}" cy="${pr * 100 + 50}" r="11" fill="#16A34A" />`
                ).join('');
                svgEl.innerHTML = `
                    <polyline points="${pts}" fill="none" stroke="#22C55E" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" opacity="0.85" />
                    ${circles}
                `;
            } else {
                svgEl.innerHTML = '';
            }
        }

        gridEl.style.gridTemplateColumns = `repeat(${colsCount}, 1fr)`;
        gridEl.style.gridTemplateRows = `repeat(${rowsCount}, 1fr)`;
        gridEl.innerHTML = '';

        grid.forEach((row, r) => {
            row.forEach((val, c) => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'maze-cell';

                const isCurrent = curR === r && curC === c;
                const isVisited = mazePath.some(([vr, vc]) => vr === r && vc === c);
                const isGoal = goal[0] === r && goal[1] === c;
                const isStart = start[0] === r && start[1] === c;
                const dR = r - curR;
                const dC = c - curC;
                const isAdjacent = Math.abs(dR) + Math.abs(dC) === 1 && !isVisited;

                let dirArrow = '';
                if (isAdjacent && currentStepIdx < steps.length) {
                    if (dR === -1) dirArrow = '↑';
                    if (dR === 1) dirArrow = '↓';
                    if (dC === -1) dirArrow = '←';
                    if (dC === 1) dirArrow = '→';
                }

                if (isCurrent) {
                    btn.classList.add('maze-cell-current');
                } else if (isVisited) {
                    btn.classList.add('maze-cell-visited');
                } else if (isAdjacent && currentStepIdx < steps.length) {
                    btn.classList.add('maze-cell-adjacent');
                }

                if (isGoal) {
                    btn.classList.add('maze-cell-goal');
                }

                let topBadge = '';
                if (isCurrent) {
                    topBadge = `<img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f680.svg" width="22" height="22" alt="Aquí" class="mb-1">`;
                } else if (isGoal) {
                    topBadge = `<img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/1f3c6.svg" width="20" height="20" alt="Meta" class="mb-1">`;
                }

                let bottomTag = '';
                if (isGoal) {
                    bottomTag = '<span class="maze-tag">Meta</span>';
                } else if (isStart) {
                    bottomTag = '<span class="maze-tag">Inicio</span>';
                } else if (isVisited) {
                    bottomTag = '<span class="maze-tag"><i class="bi bi-check-lg"></i></span>';
                }

                btn.innerHTML = `
                    <span class="maze-coord-mini">${c + 1},${r + 1}</span>
                    ${dirArrow ? `<span class="maze-dir-hint">${dirArrow}</span>` : ''}
                    ${topBadge}
                    <span class="maze-val">${val}</span>
                    ${bottomTag}
                `;

                btn.addEventListener('click', () => handleMazeCellClick(r, c, val));
                gridEl.appendChild(btn);
            });
        });
    }

    function handleMazeCellClick(r, c, val) {
        const steps = EXTRA_DATA.steps || [];
        const currentStepIdx = mazePath.length - 1;
        if (currentStepIdx >= steps.length) return;

        const [curR, curC] = mazePath[currentStepIdx];
        const isAdjacent = Math.abs(curR - r) + Math.abs(curC - c) === 1;
        const alreadyVisited = mazePath.some(([vr, vc]) => vr === r && vc === c);

        if (!isAdjacent || alreadyVisited) {
            return;
        }

        const expectedVal = steps[currentStepIdx].answer;
        if (val !== expectedVal) {
            const helper = document.getElementById('mazeHelperText');
            if (helper) {
                helper.className = 'small fw-bold text-danger mb-0';
                helper.textContent = `La casilla (X=${c + 1}, Y=${r + 1}) tiene el número ${val}, pero ${steps[currentStepIdx].expression} no da ${val}. Prueba otra dirección.`;
            }
            return;
        }

        const helper = document.getElementById('mazeHelperText');
        if (helper) {
            helper.className = 'small text-success fw-bold mb-0';
            helper.textContent = `¡Excelente! Avanzaste a (X=${c + 1}, Y=${r + 1}).`;
        }

        mazePath.push([r, c]);
        renderMathMaze();

        if (mazePath.length - 1 === steps.length) {
            postVerification({ path: mazePath });
        }
    }

    // =========================================================================
    // 5. SUDOKU VISUAL CUADRADO 4x4 (CON BLOQUES 2x2)
    // =========================================================================
    let selectedSudokuCell = null;
    const sudokuUserGrid = {};

    function initVisualSudoku() {
        const gridEl = document.getElementById('visualSudokuGrid');
        const paletteEl = document.getElementById('sudokuPalette');
        const submitBtn = document.getElementById('btnSubmitVisualSudoku');
        if (!gridEl || !paletteEl) return;

        const initial = EXTRA_DATA.initial || [];
        const items = EXTRA_DATA.items || {};

        initial.forEach((row, r) => {
            row.forEach((key, c) => {
                sudokuUserGrid[`${r},${c}`] = key || '';
                if (!key && !selectedSudokuCell) {
                    selectedSudokuCell = `${r},${c}`;
                }
            });
        });

        paletteEl.innerHTML = '';
        Object.entries(items).forEach(([itemKey, info]) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-outline-primary bg-white rounded-4 px-3 py-2 d-flex align-items-center gap-2 fw-bold sudoku-palette-btn';
            btn.innerHTML = `
                <img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/${info.icon_code || '2b50'}.svg"
                     alt="${info.label}" width="36" height="36">
                <span class="fs-6 text-dark">${info.label}</span>
            `;
            btn.addEventListener('click', () => {
                if (!selectedSudokuCell) return;
                sudokuUserGrid[selectedSudokuCell] = itemKey;
                renderSudokuGrid();
            });
            paletteEl.appendChild(btn);
        });

        const clearCellBtn = document.createElement('button');
        clearCellBtn.type = 'button';
        clearCellBtn.className = 'btn btn-outline-danger bg-white rounded-4 px-3 py-2 fw-bold sudoku-palette-btn';
        clearCellBtn.innerHTML = '<i class="bi bi-eraser-fill me-1"></i>Vaciar casilla';
        clearCellBtn.addEventListener('click', () => {
            if (!selectedSudokuCell) return;
            sudokuUserGrid[selectedSudokuCell] = '';
            renderSudokuGrid();
        });
        paletteEl.appendChild(clearCellBtn);

        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                postVerification({ grid_answers: sudokuUserGrid });
            });
        }

        renderSudokuGrid();
    }

    function renderSudokuGrid() {
        const gridEl = document.getElementById('visualSudokuGrid');
        const progressBadge = document.getElementById('sudokuProgressBadge');
        const initial = EXTRA_DATA.initial || [];
        const items = EXTRA_DATA.items || {};

        gridEl.style.gridTemplateColumns = 'repeat(4, 1fr)';
        gridEl.style.gridTemplateRows = 'repeat(4, 1fr)';
        gridEl.innerHTML = '';

        let selR = -1;
        let selC = -1;
        if (selectedSudokuCell) {
            const parts = selectedSudokuCell.split(',').map(Number);
            selR = parts[0];
            selC = parts[1];
        }

        let filledCount = 0;
        const totalCells = 16;

        initial.forEach((row, r) => {
            row.forEach((fixedKey, c) => {
                const coordKey = `${r},${c}`;
                const currentKey = sudokuUserGrid[coordKey];
                if (currentKey) filledCount += 1;

                const isFixed = Boolean(fixedKey);
                const quadIdx = Math.floor(r / 2) * 2 + Math.floor(c / 2);

                const cell = document.createElement('button');
                cell.type = 'button';
                cell.className = `sudoku-cell sudoku-quad-${quadIdx}`;

                if (r === 1) cell.classList.add('sudoku-border-bottom');
                if (c === 1) cell.classList.add('sudoku-border-right');

                if (selR !== -1 && selC !== -1) {
                    const sameRow = r === selR;
                    const sameCol = c === selC;
                    const sameQuad = Math.floor(r / 2) === Math.floor(selR / 2) && Math.floor(c / 2) === Math.floor(selC / 2);
                    if (sameRow || sameCol || sameQuad) {
                        cell.classList.add('sudoku-related');
                    }
                }

                if (isFixed) {
                    cell.classList.add('sudoku-fixed');
                    const info = items[currentKey];
                    cell.innerHTML = `
                        <div class="sudoku-fixed-badge">
                            <span class="sudoku-lock-dot"><i class="bi bi-pin-angle-fill"></i></span>
                            ${info ? `<img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/${info.icon_code || '2b50'}.svg" alt="${info.label}" width="44" height="44">` : ''}
                        </div>
                    `;
                } else {
                    cell.classList.add('sudoku-editable');
                    if (selectedSudokuCell === coordKey) {
                        cell.classList.add('sudoku-selected');
                    }
                    cell.addEventListener('click', () => {
                        selectedSudokuCell = coordKey;
                        renderSudokuGrid();
                    });

                    if (currentKey && items[currentKey]) {
                        const info = items[currentKey];
                        cell.innerHTML = `
                            <div class="sudoku-editable-slot">
                                <img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/${info.icon_code || '2b50'}.svg"
                                     alt="${info.label}" width="44" height="44">
                            </div>
                        `;
                    } else {
                        cell.innerHTML = `
                            <div class="sudoku-editable-slot">
                                <span class="fw-bold fs-4 text-primary opacity-50">?</span>
                            </div>
                        `;
                    }
                }

                gridEl.appendChild(cell);
            });
        });

        if (progressBadge) {
            progressBadge.textContent = `Completadas: ${filledCount} / ${totalCells}`;
        }
    }

    // =========================================================================
    // 6. ENCUENTRA LAS DIFERENCIAS
    // =========================================================================
    const foundDifferences = new Set();

    function initSpotDifferences() {
        const sceneA = document.getElementById('diffSceneA');
        const sceneB = document.getElementById('diffSceneB');
        if (!sceneA || !sceneB) return;

        const baseElements = EXTRA_DATA.base_elements || [];
        const differences = EXTRA_DATA.differences || [];

        updateDiffCounter();

        sceneA.innerHTML = '';
        baseElements.forEach(el => {
            sceneA.appendChild(createSceneElement(el));
        });

        sceneB.innerHTML = '';
        baseElements.forEach(el => {
            const diffOverride = differences.find(d => d.target_id === el.id);
            if (diffOverride && diffOverride.mode === 'hide') {
                return;
            }
            const merged = diffOverride && diffOverride.override
                ? { ...el, ...diffOverride.override }
                : el;
            sceneB.appendChild(createSceneElement(merged));
        });

        differences.forEach(diff => {
            if (diff.mode === 'add' && diff.element) {
                sceneB.appendChild(createSceneElement(diff.element));
            }

            const hotspot = document.createElement('button');
            hotspot.type = 'button';
            hotspot.className = 'diff-hotspot';
            hotspot.style.left = `${diff.x}%`;
            hotspot.style.top = `${diff.y}%`;
            hotspot.setAttribute('aria-label', diff.label || 'Diferencia');
            hotspot.addEventListener('click', () => handleDifferenceFound(diff, hotspot));
            sceneB.appendChild(hotspot);
        });
    }

    function createSceneElement(el) {
        const node = document.createElement('div');
        node.className = 'diff-item';
        node.style.left = `${el.x}%`;
        node.style.top = `${el.y}%`;
        const size = el.size || 44;
        const transform = el.flip ? 'translate(-50%, -50%) scaleX(-1)' : 'translate(-50%, -50%)';
        node.style.transform = transform;
        node.innerHTML = `
            <img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/${el.icon_code}.svg"
                 alt="${el.label || 'Elemento'}" width="${size}" height="${size}">
        `;
        return node;
    }

    function handleDifferenceFound(diff, hotspotEl) {
        if (foundDifferences.has(diff.id)) return;
        foundDifferences.add(diff.id);
        hotspotEl.classList.add('diff-found');

        const listEl = document.getElementById('diffFoundList');
        if (listEl) {
            const badge = document.createElement('span');
            badge.className = 'badge bg-success rounded-pill px-3 py-2';
            badge.innerHTML = `<i class="bi bi-check-circle-fill me-1"></i>${diff.label}`;
            listEl.appendChild(badge);
        }

        updateDiffCounter();

        const total = (EXTRA_DATA.differences || []).length;
        if (foundDifferences.size === total) {
            postVerification({ found_ids: Array.from(foundDifferences) });
        }
    }

    function updateDiffCounter() {
        const badge = document.getElementById('diffCounterBadge');
        const total = (EXTRA_DATA.differences || []).length;
        if (badge) {
            badge.textContent = `Encontradas: ${foundDifferences.size} / ${total}`;
        }
    }

    // =========================================================================
    // 7. PROBLEMA MATEMÁTICO CONTEXTUALIZADO
    // =========================================================================
    function initMathProblem() {
        const container = document.getElementById('mathProblemCard');
        if (!container) return;

        const contextTitle = EXTRA_DATA.context_title || 'Situación Matemática';
        const story = EXTRA_DATA.story || '';
        const items = EXTRA_DATA.items || [];
        const question = EXTRA_DATA.question || DEFAULT_QUESTION;

        container.innerHTML = `
            <div class="d-flex align-items-center gap-2 mb-2">
                <span class="badge bg-primary rounded-pill px-3 py-2">${contextTitle}</span>
            </div>
            <p class="fs-5 text-dark mb-3">${story}</p>
            ${items.length ? `
            <div class="row g-2 mb-3">
                ${items.map(it => `
                    <div class="col-6 col-sm-4">
                        <div class="bg-white rounded-3 p-2 border text-center h-100">
                            <img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/${it.icon_code || '1f6d2'}.svg"
                                 alt="${it.name}" width="40" height="40" class="mb-1">
                            <div class="fw-bold small text-dark">${it.name}</div>
                            <span class="badge bg-warning text-dark rounded-pill">${it.value}</span>
                        </div>
                    </div>
                `).join('')}
            </div>` : ''}
            <div class="bg-white rounded-3 p-3 border border-primary">
                <p class="fs-5 fw-bold text-primary mb-0">
                    <i class="bi bi-question-circle-fill me-2"></i>${question}
                </p>
            </div>
        `;
    }

    // =========================================================================
    // 8. EXPERIMENTO CASERO PASO A PASO (Ciencias)
    // =========================================================================
    function initScienceExperiment() {
        const wrapper = document.getElementById('scienceExperimentWrapper');
        const submitBtn = document.getElementById('btnSubmitScienceExperiment');
        if (!wrapper) return;

        const materials = EXTRA_DATA.materials || [];
        const steps = EXTRA_DATA.steps || [];
        const hypothesisQuestion = EXTRA_DATA.hypothesis_question || '¿Qué crees que ocurrirá en este experimento?';
        const hypothesisOptions = EXTRA_DATA.hypothesis_options || [];

        wrapper.innerHTML = `
            <div class="bg-light rounded-4 p-3 p-md-4 border mb-3">
                <h2 class="h5 fw-bold text-success mb-3">
                    <i class="bi bi-basket2-fill me-2"></i>Materiales seguros que necesitas
                </h2>
                <div class="row g-2">
                    ${materials.map(mat => `
                        <div class="col-12 col-sm-6">
                            <div class="bg-white rounded-3 p-2 px-3 border d-flex align-items-center gap-2">
                                <i class="bi bi-check2-circle text-success fs-5"></i>
                                <span class="fw-bold text-dark small">${mat}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>

            <div class="bg-light rounded-4 p-3 p-md-4 border mb-3">
                <h2 class="h5 fw-bold text-primary mb-3">
                    <i class="bi bi-list-ol me-2"></i>Procedimiento paso a paso (marca cada paso al realizarlo)
                </h2>
                <div class="d-flex flex-column gap-2">
                    ${steps.map((stepText, idx) => `
                        <label class="bg-white rounded-3 p-3 border d-flex align-items-start gap-3">
                            <input type="checkbox" class="form-check-input mt-1 flex-shrink-0" style="width: 22px; height: 22px;">
                            <span class="text-dark">
                                <strong class="text-primary">Paso ${idx + 1}:</strong> ${stepText.replace(/^Paso\s*\d+\s*:\s*/i, '')}
                            </span>
                        </label>
                    `).join('')}
                </div>
            </div>

            <div class="bg-warning bg-opacity-10 rounded-4 p-3 p-md-4 border border-2 border-warning">
                <h2 class="h5 fw-bold text-dark mb-3">
                    <i class="bi bi-clipboard2-pulse-fill text-warning me-2"></i>Ficha de Observación Científica
                </h2>

                <div class="mb-3">
                    <label class="fw-bold text-dark d-block mb-2">1. Mi Hipótesis: ${hypothesisQuestion}</label>
                    <div class="d-flex flex-column gap-2">
                        ${hypothesisOptions.map((opt, idx) => `
                            <label class="bg-white rounded-3 p-2 px-3 border d-flex align-items-center gap-2">
                                <input type="radio" name="scienceHypothesis" value="${opt}" id="hyp-${idx}" class="form-check-input">
                                <span class="fw-bold text-dark">${opt}</span>
                            </label>
                        `).join('')}
                    </div>
                </div>

                <div>
                    <label for="scienceObservationInput" class="fw-bold text-dark d-block mb-2">
                        2. Resultado final observado (escribe qué sucedió al realizar el experimento):
                    </label>
                    <textarea id="scienceObservationInput"
                              class="form-control rounded-4 border-2"
                              rows="3"
                              placeholder="Escribe aquí lo que viste ocurrir durante el experimento..."></textarea>
                </div>
            </div>
        `;

        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                const selectedRadio = document.querySelector('input[name="scienceHypothesis"]:checked');
                const observationInput = document.getElementById('scienceObservationInput');

                postVerification({
                    hypothesis: selectedRadio ? selectedRadio.value : '',
                    observation: observationInput ? observationInput.value.trim() : ''
                });
            });
        }
    }

    // =========================================================================
    // 9. CLASIFICACIÓN POR CATEGORÍAS (Ciencias)
    // =========================================================================
    let selectedSortElementId = null;
    const categoryAssignments = {};

    function initCategorySort() {
        const wrapper = document.getElementById('categorySortWrapper');
        const submitBtn = document.getElementById('btnSubmitCategorySort');
        if (!wrapper) return;

        if (submitBtn) {
            submitBtn.addEventListener('click', () => {
                postVerification({ assignments: categoryAssignments });
            });
        }
        renderCategorySort();
    }

    function renderCategorySort() {
        const wrapper = document.getElementById('categorySortWrapper');
        const categories = EXTRA_DATA.categories || [];
        const elements = EXTRA_DATA.elements || [];
        if (!wrapper) return;

        const unassigned = elements.filter(el => !categoryAssignments[el.id]);
        const colClass = categories.length >= 3 ? 'col-12 col-md-4' : 'col-12 col-md-6';

        wrapper.innerHTML = `
            <div class="bg-light rounded-4 p-3 border mb-3">
                <div class="fw-bold small text-secondary mb-2">
                    1. Toca un elemento para seleccionarlo y luego toca la categoría donde pertenece:
                </div>
                <div id="sortBank" class="d-flex flex-wrap justify-content-center gap-2">
                    ${unassigned.length ? unassigned.map(el => `
                        <button type="button"
                                class="btn ${selectedSortElementId === el.id ? 'btn-warning text-dark border-dark' : 'btn-outline-dark bg-white'} rounded-pill px-3 py-2 fw-bold d-flex align-items-center gap-2 sort-chip"
                                data-el-id="${el.id}">
                            ${el.icon_code ? `<img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/${el.icon_code}.svg" width="24" height="24" alt="${el.name}">` : ''}
                            <span>${el.name}</span>
                        </button>
                    `).join('') : '<span class="text-success fw-bold small"><i class="bi bi-check-circle-fill me-1"></i>Todos los elementos fueron ubicados en las tablas.</span>'}
                </div>
            </div>

            <div class="row g-3 text-start">
                ${categories.map(cat => {
                    const assignedHere = elements.filter(el => categoryAssignments[el.id] === cat.id);
                    return `
                        <div class="${colClass}">
                            <div class="sort-bucket h-100 rounded-4 border border-2 p-3 ${selectedSortElementId ? 'sort-bucket-ready' : ''}"
                                 data-cat-id="${cat.id}">
                                <div class="d-flex justify-content-between align-items-center border-bottom pb-2 mb-2">
                                    <h2 class="h6 fw-bold text-primary mb-0">${cat.name}</h2>
                                    <span class="badge bg-primary rounded-pill">${assignedHere.length}</span>
                                </div>
                                <div class="d-flex flex-wrap gap-2">
                                    ${assignedHere.length ? assignedHere.map(el => `
                                        <button type="button"
                                                class="btn btn-sm btn-success rounded-pill px-3 py-1 fw-bold d-flex align-items-center gap-1 remove-sort-btn"
                                                data-remove-id="${el.id}"
                                                title="Toca para devolver a la lista">
                                            ${el.icon_code ? `<img src="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/${el.icon_code}.svg" width="18" height="18" alt="${el.name}">` : ''}
                                            <span>${el.name}</span>
                                            <i class="bi bi-x-circle ms-1"></i>
                                        </button>
                                    `).join('') : '<span class="text-muted small">Toca aquí para agregar elementos</span>'}
                                </div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;

        wrapper.querySelectorAll('.sort-chip').forEach(btn => {
            btn.addEventListener('click', () => {
                const elId = btn.dataset.elId;
                selectedSortElementId = selectedSortElementId === elId ? null : elId;
                renderCategorySort();
            });
        });

        wrapper.querySelectorAll('.sort-bucket').forEach(bucket => {
            bucket.addEventListener('click', (e) => {
                if (e.target.closest('.remove-sort-btn')) return;
                if (!selectedSortElementId) return;
                categoryAssignments[selectedSortElementId] = bucket.dataset.catId;
                selectedSortElementId = null;
                renderCategorySort();
            });
        });

        wrapper.querySelectorAll('.remove-sort-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                delete categoryAssignments[btn.dataset.removeId];
                renderCategorySort();
            });
        });
    }

    // Inicializar actividad correspondiente
    if (ACTIVITY_TYPE === 'error_hunter') initErrorHunter();
    if (ACTIVITY_TYPE === 'comic_fill') initComicFill();
    if (ACTIVITY_TYPE === 'word_search') initWordGame();
    if (ACTIVITY_TYPE === 'math_maze') initMathMaze();
    if (ACTIVITY_TYPE === 'visual_sudoku') initVisualSudoku();
    if (ACTIVITY_TYPE === 'spot_differences') initSpotDifferences();
    if (ACTIVITY_TYPE === 'math_problem') initMathProblem();
    if (ACTIVITY_TYPE === 'science_experiment') initScienceExperiment();
    if (ACTIVITY_TYPE === 'category_sort') initCategorySort();
});