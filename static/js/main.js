// Основной JavaScript файл

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация
    console.log('Doc-Gen-Finance35 Web Application loaded');
    
    // Автоматическое скрытие flash сообщений
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });
    
    // Валидация форм
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#f44336';
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Пожалуйста, заполните все обязательные поля');
            }
        });
    });
    
    // Улучшение UX для JSON полей
    const jsonTextareas = document.querySelectorAll('textarea[name="table_data"], textarea[name="additional_data"]');
    jsonTextareas.forEach(textarea => {
        textarea.addEventListener('blur', function() {
            const value = this.value.trim();
            if (value) {
                try {
                    JSON.parse(value);
                    this.style.borderColor = '#4CAF50';
                } catch (e) {
                    this.style.borderColor = '#f44336';
                    console.warn('Invalid JSON:', e);
                }
            }
        });
    });
});

// Вспомогательные функции
function formatDate(date) {
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleDateString('ru-RU');
}

function validateJSON(str) {
    try {
        JSON.parse(str);
        return true;
    } catch (e) {
        return false;
    }
}

