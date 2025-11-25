# Быстрый старт - Техническая документация

## Установка

```bash
pip install -r requirements.txt
```

## Примеры использования

### 1. Документация из Python кода

```python
from doc_generator.code_analyzer import CodeAnalyzer
from doc_generator.markdown_generator import MarkdownGenerator

# Анализируем файл
analyzer = CodeAnalyzer()
code_info = analyzer.analyze_file('my_module.py')

# Генерируем Markdown
markdown_gen = MarkdownGenerator()
docs = markdown_gen.generate_code_docs(code_info, 'output.md')
```

### 2. API документация из Flask

```python
from doc_generator.api_doc_generator import APIDocGenerator

api_gen = APIDocGenerator()

# Генерируем документацию
api_info = api_gen.generate_from_flask_app('app.py')

# Markdown
md = api_gen.generate_markdown(api_info)

# OpenAPI спецификация
openapi = api_gen.generate_openapi_spec(api_info)
```

### 3. Документация базы данных

```python
from doc_generator.db_doc_generator import DBDocGenerator

db_gen = DBDocGenerator()

# Из SQL файла
db_info = db_gen.analyze_sql_file('schema.sql')

# Markdown документация
md = db_gen.generate_markdown(db_info)

# ER-диаграмма
mermaid = db_gen.generate_er_diagram_mermaid(db_info)
```

### 4. Диаграммы классов

```python
from doc_generator.code_analyzer import CodeAnalyzer
from doc_generator.diagram_generator import DiagramGenerator

analyzer = CodeAnalyzer()
diagram_gen = DiagramGenerator()

code_info = analyzer.analyze_file('my_class.py')

# Mermaid диаграмма
mermaid = diagram_gen.generate_class_diagram_mermaid(code_info)

# PlantUML диаграмма
plantuml = diagram_gen.generate_plantuml_class_diagram(code_info)
```

## Веб-интерфейс

```bash
python app_tech.py
```

Откройте http://127.0.0.1:5000

### Использование:

1. **Документация из кода:**
   - Перейдите на `/code`
   - Загрузите Python файл или ZIP архив проекта
   - Выберите формат (Markdown/JSON)
   - Скачайте документацию

2. **API документация:**
   - Перейдите на `/api`
   - Загрузите Flask приложение
   - Выберите формат (Markdown/OpenAPI)
   - Скачайте документацию

3. **Документация БД:**
   - Перейдите на `/database`
   - Загрузите SQL файл или укажите строку подключения
   - Выберите формат (Markdown/Mermaid)
   - Скачайте документацию

## Интеграция в проект

### Автоматическая генерация при коммите

Создайте `.github/workflows/docs.yml`:

```yaml
name: Generate Docs
on: [push]
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: |
          python -c "
          from doc_generator.markdown_generator import MarkdownGenerator
          MarkdownGenerator().generate_project_docs('.', 'docs/project.md')
          "
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

## Дополнительная информация

- Полная документация: [TECH_DOCUMENTATION.md](TECH_DOCUMENTATION.md)
- Примеры: см. директорию `examples/`

