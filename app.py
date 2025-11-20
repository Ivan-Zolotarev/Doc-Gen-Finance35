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
ALLOWED_EXTENSIONS = {'docx', 'xlsx', 'pdf', 'html', 'json'}


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
                if value:
                    data[key] = value
        
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
        
        # Генерация документа
        if doc_type == 'word':
            if not os.path.exists(template_path):
                # Создаем документ с нуля
                output_filename = f"document_{timestamp}_{unique_id}.docx"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                generator.word_gen.create_from_scratch(data, output_path)
            else:
                output_filename = f"document_{timestamp}_{unique_id}.docx"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                generator.generate_word(template_path, data, output_path)
            
        elif doc_type == 'pdf':
            output_filename = f"document_{timestamp}_{unique_id}.pdf"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            generator.generate_pdf(template_path, data, output_path)
            
        elif doc_type == 'excel':
            output_filename = f"document_{timestamp}_{unique_id}.xlsx"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            generator.generate_excel(template_path, data, output_path)
        else:
            return jsonify({'error': 'Неизвестный тип документа'}), 400
        
        # Возвращаем файл для скачивания
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/octet-stream'
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

