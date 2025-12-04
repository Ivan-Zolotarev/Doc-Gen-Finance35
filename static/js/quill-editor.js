// Инициализация Quill WYSIWYG редакторов

let quillEditors = {};

function initQuillEditor(editorId, placeholder = 'Введите текст...') {
    // Проверяем, не инициализирован ли уже редактор
    if (quillEditors[editorId]) {
        return quillEditors[editorId];
    }
    
    const editorElement = document.getElementById(editorId);
    if (!editorElement) return null;
    
    // Проверяем, не создан ли уже Quill на этом элементе
    if (editorElement.classList.contains('ql-container') || editorElement.querySelector('.ql-toolbar')) {
        // Quill уже инициализирован, пытаемся найти его
        const quillInstance = editorElement.__quill || editorElement.closest('.ql-editor')?.__quill;
        if (quillInstance) {
            quillEditors[editorId] = quillInstance;
            return quillInstance;
        }
    }
    
    const quill = new Quill(`#${editorId}`, {
        theme: 'snow',
        placeholder: placeholder,
        modules: {
            toolbar: [
                [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                ['bold', 'italic', 'underline', 'strike'],
                [{ 'color': [] }, { 'background': [] }],
                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                [{ 'align': [] }],
                ['link', 'image'],
                ['blockquote', 'code-block'],
                ['clean']
            ]
        }
    });
    
    quillEditors[editorId] = quill;
    return quill;
}

function getQuillContent(editorId) {
    const quill = quillEditors[editorId];
    if (!quill) return '';
    
    // Получаем HTML контент
    return quill.root.innerHTML;
}

function getQuillText(editorId) {
    const quill = quillEditors[editorId];
    if (!quill) return '';
    
    // Получаем текстовый контент
    return quill.getText();
}

function setQuillContent(editorId, htmlContent) {
    const quill = quillEditors[editorId];
    if (!quill) return;
    
    quill.root.innerHTML = htmlContent;
}

// Инициализация редакторов при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // НЕ инициализируем редакторы сразу, так как формы скрыты
    // Редакторы будут инициализированы при показе формы через showForm()
    
    // Удаляем MutationObserver, так как инициализация теперь происходит через showForm()
});

// Функция для конвертации HTML в текст для старых генераторов
function htmlToText(html) {
    const div = document.createElement('div');
    div.innerHTML = html;
    return div.textContent || div.innerText || '';
}

// Функция для сохранения HTML контента в скрытое поле перед отправкой формы
function prepareFormSubmission(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    // Обрабатываем Word форму
    if (formId === 'word-form') {
        const contentEditor = quillEditors['word-content-editor'];
        if (contentEditor) {
            const htmlContent = getQuillContent('word-content-editor');
            const textContent = getQuillText('word-content-editor');
            
            // Создаем скрытое поле для HTML
            let htmlField = form.querySelector('input[name="content_html"]');
            if (!htmlField) {
                htmlField = document.createElement('input');
                htmlField.type = 'hidden';
                htmlField.name = 'content_html';
                form.appendChild(htmlField);
            }
            htmlField.value = htmlContent;
            
            // Обновляем текстовое поле для обратной совместимости
            let textField = form.querySelector('textarea[name="content"]');
            if (textField) {
                textField.value = textContent;
            }
        }
    }
    
    // Обрабатываем PDF форму
    if (formId === 'pdf-form') {
        const contentEditor = quillEditors['pdf-content-editor'];
        if (contentEditor) {
            const htmlContent = getQuillContent('pdf-content-editor');
            const textContent = getQuillText('pdf-content-editor');
            
            // Создаем скрытое поле для HTML
            let htmlField = form.querySelector('input[name="content_html"]');
            if (!htmlField) {
                htmlField = document.createElement('input');
                htmlField.type = 'hidden';
                htmlField.name = 'content_html';
                form.appendChild(htmlField);
            }
            htmlField.value = htmlContent;
            
            // Обновляем текстовое поле
            let textField = form.querySelector('textarea[name="content"]');
            if (textField) {
                textField.value = textContent;
            }
        }
    }
}

