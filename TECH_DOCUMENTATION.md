# Техническая документация - Doc-Gen-Finance35

## Обзор

Doc-Gen-Finance35 теперь поддерживает автоматическую генерацию технической документации из:
- **Кода** - анализ Python кода, извлечение структуры, классов, функций
- **API** - автоматическая генерация документации для REST API
- **Баз данных** - схемы, ER-диаграммы, описание таблиц
- **Диаграммы** - визуализация архитектуры и структуры

## Основные возможности

### 1. Документация из кода

#### Анализ одного файла
- Парсинг структуры Python кода
- Извлечение классов, методов, функций
- Анализ docstrings (Google/NumPy стиль)
- Генерация Markdown документации

#### Анализ проекта
- Рекурсивный анализ директории
- Генерация общей документации проекта
- Диаграммы классов (Mermaid)
- Статистика по проекту

**Использование:**
```python
from doc_generator.code_analyzer import CodeAnalyzer
from doc_generator.markdown_generator import MarkdownGenerator

analyzer = CodeAnalyzer()
markdown_gen = MarkdownGenerator()

# Анализ файла
code_info = analyzer.analyze_file('my_module.py')
docs = markdown_gen.generate_code_docs(code_info, 'output.md')

# Анализ проекта
project_docs = markdown_gen.generate_project_docs('project/', 'project_docs.md')
```

### 2. API документация

#### Поддерживаемые форматы:
- **Markdown** - читаемая документация
- **OpenAPI 3.0** - для Swagger UI, Postman

#### Функции:
- Автоматическое извлечение Flask маршрутов
- Анализ параметров и типов
- Генерация OpenAPI спецификаций
- Описание endpoints

**Использование:**
```python
from doc_generator.api_doc_generator import APIDocGenerator

api_gen = APIDocGenerator()

# Генерация из Flask приложения
api_info = api_gen.generate_from_flask_app('app.py')

# Markdown документация
md = api_gen.generate_markdown(api_info)

# OpenAPI спецификация
openapi_spec = api_gen.generate_openapi_spec(api_info)
```

### 3. Документация баз данных

#### Источники данных:
- SQL файлы (CREATE TABLE, DDL)
- Прямое подключение к БД (PostgreSQL, MySQL, SQLite)

#### Генерируемая документация:
- Описание всех таблиц
- Структура колонок и типы данных
- Первичные и внешние ключи
- Индексы и ограничения
- ER-диаграммы (Mermaid)

**Использование:**
```python
from doc_generator.db_doc_generator import DBDocGenerator

db_gen = DBDocGenerator()

# Из SQL файла
db_info = db_gen.analyze_sql_file('schema.sql')

# Из подключения
db_info = db_gen.analyze_database('postgresql://user:pass@localhost/db')

# Markdown документация
md = db_gen.generate_markdown(db_info)

# ER-диаграмма
mermaid = db_gen.generate_er_diagram_mermaid(db_info)
```

### 4. Генерация диаграмм

#### Поддерживаемые типы:
- **Диаграммы классов** (Mermaid, PlantUML)
- **ER-диаграммы** (Mermaid)
- **Блок-схемы** (Mermaid)
- **Диаграммы последовательности** (Mermaid)
- **Архитектурные диаграммы** (Mermaid)

**Использование:**
```python
from doc_generator.diagram_generator import DiagramGenerator
from doc_generator.code_analyzer import CodeAnalyzer

diagram_gen = DiagramGenerator()
analyzer = CodeAnalyzer()

code_info = analyzer.analyze_file('my_class.py')

# Диаграмма классов
class_diagram = diagram_gen.generate_class_diagram_mermaid(code_info)

# PlantUML диаграмма
plantuml = diagram_gen.generate_plantuml_class_diagram(code_info)
```

## Веб-интерфейс

### Запуск
```bash
python app_tech.py
```

Откройте в браузере: http://127.0.0.1:5000

### Страницы:
- **/** - Главная страница с выбором типа документации
- **/code** - Генерация документации из кода
- **/api** - Генерация API документации
- **/database** - Генерация документации БД

### API Endpoints:

#### POST /analyze-code
Анализ одного файла с кодом
- `code_file` - Python файл
- `format` - markdown или json

#### POST /analyze-project
Анализ проекта (ZIP архив)
- `project_zip` - ZIP архив с Python файлами

#### POST /generate-api-docs
Генерация API документации
- `api_file` - Flask приложение
- `format` - markdown или openapi

#### POST /generate-db-docs
Генерация документации БД
- `db_type` - sql_file или connection
- `sql_file` или `connection_string`
- `format` - markdown или mermaid

#### POST /generate-diagram
Генерация диаграммы
- `code_file` - Python файл
- `diagram_type` - class, flowchart, sequence

## Форматы вывода

### Markdown
Структурированная документация с:
- Заголовками и подзаголовками
- Таблицами
- Блоками кода
- Списками

### JSON
Структурированные данные для:
- Дальнейшей обработки
- Интеграции с другими инструментами
- Программного доступа

### OpenAPI
Спецификация для:
- Swagger UI
- Postman
- Других API инструментов

### Mermaid
Диаграммы для:
- GitHub/GitLab
- Документации
- Визуализации

## Примеры использования

### Пример 1: Документация модуля

```python
from doc_generator.code_analyzer import CodeAnalyzer
from doc_generator.markdown_generator import MarkdownGenerator

analyzer = CodeAnalyzer()
markdown_gen = MarkdownGenerator()

# Анализируем модуль
code_info = analyzer.analyze_file('my_module.py')

# Генерируем документацию
docs = markdown_gen.generate_code_docs(code_info, 'my_module_docs.md')
print("Документация создана: my_module_docs.md")
```

### Пример 2: API документация

```python
from doc_generator.api_doc_generator import APIDocGenerator

api_gen = APIDocGenerator()

# Генерируем из Flask приложения
api_info = api_gen.generate_from_flask_app('app.py')

# Создаем OpenAPI спецификацию
openapi = api_gen.generate_openapi_spec(api_info)

# Сохраняем
import json
with open('api_spec.json', 'w') as f:
    json.dump(openapi, f, indent=2)
```

### Пример 3: Документация БД

```python
from doc_generator.db_doc_generator import DBDocGenerator

db_gen = DBDocGenerator()

# Анализируем SQL файл
db_info = db_gen.analyze_sql_file('schema.sql')

# Генерируем ER-диаграмму
mermaid = db_gen.generate_er_diagram_mermaid(db_info)

# Сохраняем
with open('er_diagram.mmd', 'w') as f:
    f.write(mermaid)
```

## Интеграция в CI/CD

### GitHub Actions пример:

```yaml
name: Generate Documentation

on:
  push:
    branches: [ main ]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Generate docs
        run: |
          python -c "
          from doc_generator.markdown_generator import MarkdownGenerator
          gen = MarkdownGenerator()
          gen.generate_project_docs('.', 'docs/project_docs.md')
          "
      - name: Commit docs
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add docs/
          git commit -m "Update documentation" || exit 0
          git push
```

## Расширение функциональности

### Добавление поддержки нового языка

1. Расширьте `CodeAnalyzer` для поддержки нового языка
2. Добавьте парсер для синтаксиса
3. Обновите генераторы документации

### Добавление нового типа диаграммы

1. Создайте метод в `DiagramGenerator`
2. Добавьте поддержку в веб-интерфейс
3. Обновите документацию

## Ограничения

1. **Python код** - полная поддержка только Python, другие языки требуют расширения
2. **Flask API** - поддержка только Flask, другие фреймворки требуют адаптации
3. **Базы данных** - требуется SQLAlchemy для прямого подключения
4. **Диаграммы** - Mermaid требует поддержки в среде просмотра

## Планы развития

- [ ] Поддержка других языков программирования (JavaScript, Java, Go)
- [ ] Поддержка других веб-фреймворков (Django, FastAPI)
- [ ] Интеграция с Git для автоматического обновления
- [ ] Веб-просмотрщик документации
- [ ] Экспорт в PDF с форматированием
- [ ] Поддержка PlantUML для всех типов диаграмм
- [ ] Интеграция с Jira, Confluence
- [ ] Автоматическое обновление документации при коммитах

## Автор

Разработано в рамках производственной практики  
ООО "Система Связи"

