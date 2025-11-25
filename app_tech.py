"""
Flask веб-приложение для автоматической генерации технической документации
Расширенная версия с поддержкой анализа кода, API, БД
"""

import os
import sys
import zipfile
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import uuid
import tempfile
import shutil

# Добавляем корневую директорию в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from doc_generator import DocumentGenerator
from doc_generator.code_analyzer import CodeAnalyzer
from doc_generator.api_doc_generator import APIDocGenerator
from doc_generator.db_doc_generator import DBDocGenerator
from doc_generator.markdown_generator import MarkdownGenerator
from doc_generator.diagram_generator import DiagramGenerator

app = Flask(__name__)
app.secret_key = 'doc-gen-finance35-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['TEMP_FOLDER'] = 'temp'

# Создаем необходимые директории
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Инициализация генераторов
generator = DocumentGenerator(output_dir=app.config['OUTPUT_FOLDER'])
code_analyzer = CodeAnalyzer()
api_generator = APIDocGenerator()
db_generator = DBDocGenerator()
markdown_generator = MarkdownGenerator()
diagram_generator = DiagramGenerator()

# Разрешенные расширения файлов
ALLOWED_CODE_EXTENSIONS = {'py', 'js', 'java', 'cpp', 'c', 'h', 'hpp', 'cs', 'go', 'rs', 'php', 'rb', 'ts'}
ALLOWED_DB_EXTENSIONS = {'sql', 'db', 'sqlite', 'sqlite3'}


def allowed_file(filename, extensions):
    """Проверка разрешенного расширения файла"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@app.route('/')
def index():
    """Главная страница"""
    return render_template('tech_index.html')


@app.route('/old')
def old_index():
    """Старая версия (для обратной совместимости)"""
    try:
        return render_template('index.html')
    except:
        return redirect(url_for('index'))


@app.route('/code')
def code_docs():
    """Страница генерации документации из кода"""
    return render_template('code_docs.html')


@app.route('/api')
def api_docs():
    """Страница генерации API документации"""
    return render_template('api_docs.html')


@app.route('/database')
def database_docs():
    """Страница генерации документации БД"""
    return render_template('database_docs.html')


@app.route('/analyze-code', methods=['POST'])
def analyze_code():
    """Анализ кода и генерация документации"""
    try:
        if 'code_file' not in request.files:
            return jsonify({'error': 'Файл не загружен'}), 400
        
        file = request.files['code_file']
        if file.filename == '':
            return jsonify({'error': 'Файл не выбран'}), 400
        
        if not allowed_file(file.filename, ALLOWED_CODE_EXTENSIONS):
            return jsonify({'error': 'Неподдерживаемый формат файла'}), 400
        
        # Сохраняем файл
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['TEMP_FOLDER'], f"{uuid.uuid4()}_{filename}")
        file.save(file_path)
        
        # Анализируем код
        if filename.endswith('.py'):
            code_info = code_analyzer.analyze_file(file_path)
        else:
            return jsonify({'error': 'Пока поддерживается только Python код'}), 400
        
        # Генерируем документацию
        output_format = request.form.get('format', 'markdown')
        
        if output_format == 'markdown':
            md_content = markdown_generator.generate_code_docs(code_info)
            output_filename = f"docs_{filename.rsplit('.', 1)[0]}.md"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        
        elif output_format == 'json':
            output_filename = f"docs_{filename.rsplit('.', 1)[0]}.json"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(code_info, f, ensure_ascii=False, indent=2)
            
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        
        else:
            return jsonify({'error': 'Неподдерживаемый формат вывода'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/analyze-project', methods=['POST'])
def analyze_project():
    """Анализ проекта и генерация документации"""
    try:
        if 'project_zip' not in request.files:
            return jsonify({'error': 'Архив проекта не загружен'}), 400
        
        file = request.files['project_zip']
        if file.filename == '':
            return jsonify({'error': 'Архив не выбран'}), 400
        
        # Создаем временную директорию
        temp_dir = os.path.join(app.config['TEMP_FOLDER'], str(uuid.uuid4()))
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Распаковываем архив
            zip_path = os.path.join(temp_dir, 'project.zip')
            file.save(zip_path)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Анализируем проект
            try:
                md_content = markdown_generator.generate_project_docs(temp_dir)
            except Exception as e:
                return jsonify({'error': f'Ошибка при генерации документации: {str(e)}'}), 500
            
            # Генерируем диаграммы
            try:
                analysis = code_analyzer.analyze_directory(temp_dir)
                diagrams = {}
                
                for file_info in analysis.get('files', []):
                    try:
                        # Пропускаем файлы с ошибками
                        if 'error' in file_info:
                            continue
                        
                        # Проверяем наличие классов
                        if file_info.get('classes') and len(file_info.get('classes', [])) > 0:
                            try:
                                class_diagram = diagram_generator.generate_class_diagram_mermaid(file_info)
                                if class_diagram:
                                    file_name = file_info.get('file', 'unknown')
                                    diagrams[file_name] = class_diagram
                            except Exception as e:
                                # Пропускаем файлы, для которых не удалось создать диаграмму
                                print(f"Не удалось создать диаграмму для {file_info.get('file', 'unknown')}: {e}")
                                continue
                    except Exception as e:
                        # Пропускаем проблемные файлы
                        print(f"Ошибка при обработке файла: {e}")
                        continue
            except Exception as e:
                # Если не удалось создать диаграммы, продолжаем без них
                print(f"Ошибка при генерации диаграмм: {e}")
                diagrams = {}
            
            # Сохраняем результат
            output_filename = f"project_docs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
                if diagrams:
                    f.write("\n\n## Diagrams\n\n")
                    for file_name, diagram in diagrams.items():
                        f.write(f"### {file_name}\n\n")
                        f.write("```mermaid\n")
                        f.write(diagram)
                        f.write("\n```\n\n")
            
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        
        finally:
            # Удаляем временную директорию
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-api-docs', methods=['POST'])
def generate_api_docs():
    """Генерация API документации"""
    try:
        if 'api_file' not in request.files:
            return jsonify({'error': 'Файл не загружен'}), 400
        
        file = request.files['api_file']
        if file.filename == '':
            return jsonify({'error': 'Файл не выбран'}), 400
        
        if not file.filename.endswith('.py'):
            return jsonify({'error': 'Поддерживаются только Python файлы'}), 400
        
        # Сохраняем файл
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['TEMP_FOLDER'], f"{uuid.uuid4()}_{filename}")
        file.save(file_path)
        
        # Генерируем API документацию
        api_info = api_generator.generate_from_flask_app(file_path)
        output_format = request.form.get('format', 'markdown')
        
        if output_format == 'markdown':
            md_content = api_generator.generate_markdown(api_info)
            output_filename = f"api_docs_{filename.rsplit('.', 1)[0]}.md"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        
        elif output_format == 'openapi':
            openapi_spec = api_generator.generate_openapi_spec(api_info)
            output_filename = f"api_spec_{filename.rsplit('.', 1)[0]}.json"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(openapi_spec, f, ensure_ascii=False, indent=2)
            
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        
        else:
            return jsonify({'error': 'Неподдерживаемый формат вывода'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-db-docs', methods=['POST'])
def generate_db_docs():
    """Генерация документации БД"""
    try:
        db_type = request.form.get('db_type', 'sql_file')
        
        if db_type == 'sql_file':
            if 'sql_file' not in request.files:
                return jsonify({'error': 'SQL файл не загружен'}), 400
            
            file = request.files['sql_file']
            if file.filename == '':
                return jsonify({'error': 'Файл не выбран'}), 400
            
            if not allowed_file(file.filename, ALLOWED_DB_EXTENSIONS):
                return jsonify({'error': 'Неподдерживаемый формат файла'}), 400
            
            # Сохраняем файл
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['TEMP_FOLDER'], f"{uuid.uuid4()}_{filename}")
            file.save(file_path)
            
            # Анализируем SQL
            db_info = db_generator.analyze_sql_file(file_path)
        
        elif db_type == 'connection':
            connection_string = request.form.get('connection_string', '')
            if not connection_string:
                return jsonify({'error': 'Строка подключения не указана'}), 400
            
            db_info = db_generator.analyze_database(connection_string)
        
        else:
            return jsonify({'error': 'Неподдерживаемый тип источника БД'}), 400
        
        # Генерируем документацию
        output_format = request.form.get('format', 'markdown')
        
        if output_format == 'markdown':
            md_content = db_generator.generate_markdown(db_info)
            output_filename = f"db_docs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        
        elif output_format == 'mermaid':
            mermaid_diagram = db_generator.generate_er_diagram_mermaid(db_info)
            output_filename = f"db_diagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mmd"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(mermaid_diagram)
            
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        
        else:
            return jsonify({'error': 'Неподдерживаемый формат вывода'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-diagram', methods=['POST'])
def generate_diagram():
    """Генерация диаграммы из кода"""
    try:
        if 'code_file' not in request.files:
            return jsonify({'error': 'Файл не загружен'}), 400
        
        file = request.files['code_file']
        if file.filename == '':
            return jsonify({'error': 'Файл не выбран'}), 400
        
        if not file.filename.endswith('.py'):
            return jsonify({'error': 'Поддерживаются только Python файлы'}), 400
        
        # Сохраняем файл
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['TEMP_FOLDER'], f"{uuid.uuid4()}_{filename}")
        file.save(file_path)
        
        # Анализируем код
        code_info = code_analyzer.analyze_file(file_path)
        diagram_type = request.form.get('diagram_type', 'class')
        
        if diagram_type == 'class':
            diagram = diagram_generator.generate_class_diagram_mermaid(code_info)
        else:
            return jsonify({'error': 'Неподдерживаемый тип диаграммы'}), 400
        
        output_filename = f"diagram_{filename.rsplit('.', 1)[0]}.mmd"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(diagram)
        
        return send_file(output_path, as_attachment=True, download_name=output_filename)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Старые маршруты для обратной совместимости
@app.route('/generate', methods=['POST'])
def generate_document():
    """Генерация документа (старый API)"""
    # Перенаправляем на главную страницу
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("=" * 50)
    print("Doc-Gen-Finance35 Technical Documentation Generator")
    print("=" * 50)
    print("Откройте в браузере: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)

