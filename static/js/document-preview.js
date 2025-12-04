// Предпросмотр документа в реальном времени

function initDocumentPreview() {
    // Предпросмотр для Word формы
    const wordForm = document.getElementById('word-form');
    if (wordForm) {
        setupWordPreview(wordForm);
    }
    
    // Предпросмотр для PDF формы
    const pdfForm = document.getElementById('pdf-form');
    if (pdfForm) {
        setupPDFPreview(pdfForm);
    }
}

function setupWordPreview(form) {
    // Создаем контейнер для предпросмотра
    const contentGroup = form.querySelector('#word-content-editor').closest('.form-group');
    if (!contentGroup) return;
    
    // Проверяем, не создан ли уже предпросмотр
    if (contentGroup.querySelector('.document-preview')) return;
    
    const previewContainer = document.createElement('div');
    previewContainer.className = 'document-preview';
    previewContainer.innerHTML = `
        <div class="preview-header">
            <h4>📄 Предпросмотр документа</h4>
            <button type="button" class="preview-toggle" onclick="togglePreview(this)">
                <span class="preview-icon">▼</span> Свернуть
            </button>
        </div>
        <div class="preview-content word-preview">
            <div class="preview-document">
                <div class="preview-title" id="preview-word-title">ДОГОВОР</div>
                <div class="preview-section">
                    <div class="preview-field">
                        <strong>Номер договора:</strong> 
                        <span id="preview-word-contract-number" class="preview-value">ДГ-2024-001</span>
                    </div>
                    <div class="preview-field">
                        <strong>Дата:</strong> 
                        <span id="preview-word-date" class="preview-value">20.12.2024</span>
                    </div>
                </div>
                <div class="preview-section">
                    <div class="preview-field">
                        <strong>Сторона 1 (Заказчик):</strong> 
                        <span id="preview-word-party1" class="preview-value">ООО 'Компания'</span>
                    </div>
                    <div class="preview-field">
                        <strong>Сторона 2 (Исполнитель):</strong> 
                        <span id="preview-word-party2" class="preview-value">ООО 'Система Связи'</span>
                    </div>
                </div>
                <div class="preview-section">
                    <div class="preview-field">
                        <strong>Предмет договора:</strong>
                        <div id="preview-word-subject" class="preview-value preview-text">Описание предмета договора</div>
                    </div>
                </div>
                <div class="preview-section">
                    <div class="preview-field">
                        <strong>Сумма:</strong> 
                        <span id="preview-word-amount" class="preview-value">500 000</span> руб.
                    </div>
                    <div class="preview-field">
                        <strong>Срок выполнения:</strong> 
                        <span id="preview-word-deadline" class="preview-value">31.12.2024</span>
                    </div>
                </div>
                <div class="preview-section">
                    <div class="preview-field">
                        <strong>Дополнительное содержимое:</strong>
                        <div id="preview-word-content" class="preview-value preview-html-content">
                            <p>Дополнительный текст документа...</p>
                        </div>
                    </div>
                </div>
                <div class="preview-section preview-signatures">
                    <div class="preview-field">
                        <strong>Подпись заказчика:</strong> 
                        <span id="preview-word-customer" class="preview-value">Иванов И.И.</span>
                    </div>
                    <div class="preview-field">
                        <strong>Подпись исполнителя:</strong> 
                        <span id="preview-word-executor" class="preview-value">Веселенко Т.Н.</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    contentGroup.appendChild(previewContainer);
    
    // Подписываемся на изменения в форме
    const inputs = form.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', () => updateWordPreview(form));
        input.addEventListener('change', () => updateWordPreview(form));
    });
    
    // Подписываемся на изменения в Quill редакторе
    if (window.quillEditors && window.quillEditors['word-content-editor']) {
        window.quillEditors['word-content-editor'].on('text-change', () => {
            updateWordPreview(form);
        });
    }
    
    // Обновляем при показе формы
    setTimeout(() => updateWordPreview(form), 100);
}

function setupPDFPreview(form) {
    const contentGroup = form.querySelector('#pdf-content-editor').closest('.form-group');
    if (!contentGroup) return;
    
    if (contentGroup.querySelector('.document-preview')) return;
    
    const previewContainer = document.createElement('div');
    previewContainer.className = 'document-preview';
    previewContainer.innerHTML = `
        <div class="preview-header">
            <h4>📄 Предпросмотр PDF</h4>
            <button type="button" class="preview-toggle" onclick="togglePreview(this)">
                <span class="preview-icon">▼</span> Свернуть
            </button>
        </div>
        <div class="preview-content pdf-preview">
            <div class="preview-document">
                <div class="preview-title" id="preview-pdf-title">Финансовый отчет</div>
                <div class="preview-section">
                    <div class="preview-field">
                        <strong>Дата:</strong> 
                        <span id="preview-pdf-date" class="preview-value">20.12.2024</span>
                    </div>
                </div>
                <div class="preview-section">
                    <div class="preview-field">
                        <strong>Содержимое:</strong>
                        <div id="preview-pdf-content" class="preview-value preview-html-content">
                            <p>Текст документа...</p>
                        </div>
                    </div>
                </div>
                <div class="preview-section preview-signatures">
                    <div class="preview-field">
                        <strong>Подпись:</strong> 
                        <span id="preview-pdf-signature" class="preview-value">Иванов И.И.</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    contentGroup.appendChild(previewContainer);
    
    const inputs = form.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', () => updatePDFPreview(form));
        input.addEventListener('change', () => updatePDFPreview(form));
    });
    
    if (window.quillEditors && window.quillEditors['pdf-content-editor']) {
        window.quillEditors['pdf-content-editor'].on('text-change', () => {
            updatePDFPreview(form);
        });
    }
    
    setTimeout(() => updatePDFPreview(form), 100);
}

function updateWordPreview(form) {
    // Обновляем номер договора
    const contractNumber = form.querySelector('input[name="contract_number"]')?.value || 'ДГ-2024-001';
    updatePreviewField('preview-word-contract-number', contractNumber || 'Не указан');
    
    // Обновляем дату
    const dateInput = form.querySelector('input[name="date"]');
    let dateValue = '20.12.2024';
    if (dateInput && dateInput.value) {
        const date = new Date(dateInput.value);
        dateValue = date.toLocaleDateString('ru-RU');
    }
    updatePreviewField('preview-word-date', dateValue);
    
    // Обновляем стороны
    updatePreviewField('preview-word-party1', form.querySelector('input[name="party1_name"]')?.value || 'ООО \'Компания\'');
    updatePreviewField('preview-word-party2', form.querySelector('input[name="party2_name"]')?.value || 'ООО \'Система Связи\'');
    
    // Обновляем предмет договора
    const subject = form.querySelector('textarea[name="subject"]')?.value || 'Описание предмета договора';
    updatePreviewField('preview-word-subject', subject, true);
    
    // Обновляем сумму и срок
    updatePreviewField('preview-word-amount', form.querySelector('input[name="amount"]')?.value || '500 000');
    
    const deadlineInput = form.querySelector('input[name="deadline"]');
    let deadlineValue = '31.12.2024';
    if (deadlineInput && deadlineInput.value) {
        const date = new Date(deadlineInput.value);
        deadlineValue = date.toLocaleDateString('ru-RU');
    }
    updatePreviewField('preview-word-deadline', deadlineValue);
    
    // Обновляем подписи
    updatePreviewField('preview-word-customer', form.querySelector('input[name="customer_signature"]')?.value || 'Иванов И.И.');
    updatePreviewField('preview-word-executor', form.querySelector('input[name="executor_signature"]')?.value || 'Веселенко Т.Н.');
    
    // Обновляем содержимое из WYSIWYG редактора
    const contentEditor = window.quillEditors && window.quillEditors['word-content-editor'];
    if (contentEditor) {
        const htmlContent = window.getQuillContent('word-content-editor');
        const contentElement = document.getElementById('preview-word-content');
        if (contentElement) {
            if (htmlContent && htmlContent.trim() !== '<p><br></p>') {
                contentElement.innerHTML = htmlContent;
            } else {
                contentElement.innerHTML = '<p class="preview-placeholder">Дополнительный текст документа...</p>';
            }
        }
    } else {
        const textContent = form.querySelector('textarea[name="content"]')?.value;
        const contentElement = document.getElementById('preview-word-content');
        if (contentElement) {
            if (textContent && textContent.trim()) {
                contentElement.innerHTML = '<p>' + textContent.replace(/\n/g, '</p><p>') + '</p>';
            } else {
                contentElement.innerHTML = '<p class="preview-placeholder">Дополнительный текст документа...</p>';
            }
        }
    }
}

function updatePDFPreview(form) {
    // Обновляем заголовок
    updatePreviewField('preview-pdf-title', form.querySelector('input[name="title"]')?.value || 'Финансовый отчет');
    
    // Обновляем дату
    const dateInput = form.querySelector('input[name="date"]');
    let dateValue = '20.12.2024';
    if (dateInput && dateInput.value) {
        const date = new Date(dateInput.value);
        dateValue = date.toLocaleDateString('ru-RU');
    }
    updatePreviewField('preview-pdf-date', dateValue);
    
    // Обновляем содержимое
    const contentEditor = window.quillEditors && window.quillEditors['pdf-content-editor'];
    if (contentEditor) {
        const htmlContent = window.getQuillContent('pdf-content-editor');
        const contentElement = document.getElementById('preview-pdf-content');
        if (contentElement) {
            if (htmlContent && htmlContent.trim() !== '<p><br></p>') {
                contentElement.innerHTML = htmlContent;
            } else {
                contentElement.innerHTML = '<p class="preview-placeholder">Текст документа...</p>';
            }
        }
    } else {
        const textContent = form.querySelector('textarea[name="content"]')?.value;
        const contentElement = document.getElementById('preview-pdf-content');
        if (contentElement) {
            if (textContent && textContent.trim()) {
                contentElement.innerHTML = '<p>' + textContent.replace(/\n/g, '</p><p>') + '</p>';
            } else {
                contentElement.innerHTML = '<p class="preview-placeholder">Текст документа...</p>';
            }
        }
    }
    
    // Обновляем подпись
    updatePreviewField('preview-pdf-signature', form.querySelector('input[name="signature"]')?.value || 'Иванов И.И.');
}

function updatePreviewField(id, value, isTextarea = false) {
    const element = document.getElementById(id);
    if (!element) return;
    
    if (isTextarea) {
        element.textContent = value || 'Не указано';
    } else {
        element.textContent = value || 'Не указано';
    }
}

function togglePreview(button) {
    const preview = button.closest('.document-preview');
    const content = preview.querySelector('.preview-content');
    const icon = button.querySelector('.preview-icon');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        icon.textContent = '▼';
        button.innerHTML = '<span class="preview-icon">▼</span> Свернуть';
    } else {
        content.style.display = 'none';
        icon.textContent = '▶';
        button.innerHTML = '<span class="preview-icon">▶</span> Развернуть';
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Ждем инициализации Quill
    setTimeout(() => {
        initDocumentPreview();
    }, 500);
    
    // Инициализируем при показе формы
    const originalShowForm = window.showForm;
    if (originalShowForm) {
        window.showForm = function(type) {
            originalShowForm(type);
            setTimeout(() => {
                initDocumentPreview();
            }, 200);
        };
    }
});

