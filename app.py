"""
Flask веб-приложение для генерации документов
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import uuid

# Добавляем корневую директорию в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from doc_generator import DocumentGenerator
from docx2pdf import convert as docx_to_pdf

app = Flask(__name__)
app.secret_key = 'doc-gen-finance35-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Создаем необходимые директории
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Инициализация генератора
generator = DocumentGenerator(output_dir=app.config['OUTPUT_FOLDER'])

# Разрешенные расширения файлов
ALLOWED_EXTENSIONS = {'docx', 'json'}


def allowed_file(filename):
    """Проверка разрешенного расширения файла"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_document():
    """Генерация документа"""
    try:
        doc_type = request.form.get('doc_type')
        
        if not doc_type:
            return jsonify({'error': 'Тип документа не указан'}), 400
        
        # Получаем данные из формы
        data = {}
        for key, value in request.form.items():
            if key != 'doc_type' and key != 'template_file':
                # Сохраняем все значения, даже пустые (для замены плейсхолдеров)
                data[key] = value if value else ''
        
        # Обрабатываем дату - преобразуем из YYYY-MM-DD в DD.MM.YYYY
        if 'date' in data and data['date']:
            try:
                date_obj = datetime.strptime(data['date'], '%Y-%m-%d')
                data['date'] = date_obj.strftime('%d.%m.%Y')
            except Exception as e:
                # Если не удалось преобразовать, оставляем как есть
                print(f"Ошибка преобразования даты: {e}")
        
        # Обрабатываем deadline аналогично
        if 'deadline' in data and data['deadline']:
            try:
                date_obj = datetime.strptime(data['deadline'], '%Y-%m-%d')
                data['deadline'] = date_obj.strftime('%d.%m.%Y')
            except Exception as e:
                print(f"Ошибка преобразования deadline: {e}")
        
        # Отладочный вывод (можно убрать в production)
        print(f"Данные для генерации: {data}")
        
        # Приоритет HTML контенту из WYSIWYG редактора
        if 'content_html' in data and data['content_html']:
            # HTML контент уже в data, оставляем его
            pass
        elif 'content' in data:
            # Используем текстовый контент
            pass
        
        # Обработка табличных данных (если есть)
        if 'table_data' in request.form:
            try:
                table_data = json.loads(request.form['table_data'])
                data['table_data'] = table_data
            except:
                pass
        
        # Генерация уникального имени файла
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        
        # Обработка загруженного шаблона
        template_path = None
        if 'template_file' in request.files:
            file = request.files['template_file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                template_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
                file.save(template_path)
        
        # Если шаблон не загружен, используем стандартный
        if not template_path:
            if doc_type == 'word':
                template_path = 'templates/contract_template.docx'
            elif doc_type == 'excel':
                template_path = None  # Excel можно создавать без шаблона
        
        # Генерация документа (только Word) с опциональной конвертацией в PDF
        if doc_type == 'word':
            if not template_path or not os.path.exists(template_path):
                output_filename = f"document_{timestamp}_{unique_id}.docx"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                print(f"Создание документа с нуля. Данные: {data}")
                generator.word_gen.create_from_scratch(data, output_path)
            else:
                output_filename = f"document_{timestamp}_{unique_id}.docx"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                print(f"Используется шаблон: {template_path}")
                print(f"Данные для замены: {data}")
                generator.generate_word(template_path, data, output_path)

            # Конвертация в PDF, если запрошено
            convert_to_pdf = request.form.get('convert_to_pdf') == 'on'
            if convert_to_pdf:
                try:
                    pdf_filename = output_filename.replace('.docx', '.pdf')
                    pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
                    docx_to_pdf(output_path, pdf_path)
                    # Отдаем PDF
                    return send_file(
                        pdf_path,
                        as_attachment=True,
                        download_name=pdf_filename,
                        mimetype='application/pdf'
                    )
                except Exception as e:
                    print(f"Не удалось конвертировать в PDF: {e}. Отправляем DOCX.")

        else:
            return jsonify({'error': 'Поддерживается только тип документа word'}), 400
        
        # Возвращаем файл для скачивания (DOCX)
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/templates')
def templates_page():
    """Страница со списком доступных шаблонов"""
    templates = []
    templates_dir = Path('templates')
    
    if templates_dir.exists():
        for file in templates_dir.glob('*.docx'):
            templates.append({
                'name': file.name,
                'type': 'word',
                'path': str(file)
            })
        for file in templates_dir.glob('*.html'):
            templates.append({
                'name': file.name,
                'type': 'pdf',
                'path': str(file)
            })
    
    return render_template('templates.html', templates=templates)


@app.route('/api/templates')
def api_templates():
    """API для получения списка шаблонов"""
    templates = []
    templates_dir = Path('templates')
    
    if templates_dir.exists():
        for file in templates_dir.glob('*.docx'):
            templates.append({
                'name': file.name,
                'type': 'word',
                'path': str(file)
            })
    
    return jsonify(templates)


@app.route('/health')
def health():
    """Проверка работоспособности"""
    return jsonify({'status': 'ok', 'message': 'Doc-Gen-Finance35 работает'})


if __name__ == '__main__':
    print("=" * 50)
    print("Doc-Gen-Finance35 Web Application")
    print("=" * 50)
    print("Откройте в браузере: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)

