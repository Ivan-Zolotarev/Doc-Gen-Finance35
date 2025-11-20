# Документация проекта Doc-Gen-Finance35

## Описание

Doc-Gen-Finance35 - это система автоматической генерации документов, разработанная для упрощения процесса создания различных типов документов (договоры, отчеты, справки и т.д.) на основе шаблонов и данных.

## Архитектура системы

### Основные компоненты

1. **DocumentGenerator** - главный класс для работы с генерацией документов
2. **WordGenerator** - генератор документов Word (.docx)
3. **PDFGenerator** - генератор документов PDF
4. **ExcelGenerator** - генератор документов Excel (.xlsx)

### Структура проекта

```
Doc-Gen-Finance35/
├── doc_generator/          # Основной модуль
│   ├── __init__.py
│   ├── generator.py        # Главный класс генератора
│   ├── word_generator.py   # Генератор Word
│   ├── pdf_generator.py    # Генератор PDF
│   └── excel_generator.py  # Генератор Excel
├── templates/              # Шаблоны документов
│   ├── create_templates.py # Скрипт создания шаблонов
│   └── report_template.html
├── data/                   # Исходные данные
│   └── sample_data.json
├── config/                 # Конфигурационные файлы
│   └── generation_config.json
├── examples/               # Примеры использования
│   ├── basic_example.py
│   └── config_example.py
├── output/                 # Сгенерированные документы
├── main.py                 # Главный файл запуска
├── requirements.txt        # Зависимости
└── README.md              # Основная документация
```

## Установка

### Требования

- Python 3.7 или выше
- pip

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Создание шаблонов

Перед использованием необходимо создать шаблоны документов:

```bash
python templates/create_templates.py
```

Это создаст следующие шаблоны:
- `templates/contract_template.docx` - шаблон договора
- `templates/report_template.docx` - шаблон финансового отчета
- `templates/certificate_template.docx` - шаблон справки

## Использование

### Базовое использование

```python
from doc_generator import DocumentGenerator

# Инициализация генератора
generator = DocumentGenerator(output_dir="output")

# Данные для документа
data = {
    "contract_number": "ДГ-2024-001",
    "date": "20.12.2024",
    "party1_name": "ООО 'Система Связи'",
    "party2_name": "ООО 'Клиент'",
    "subject": "Разработка ПО",
    "amount": "500 000",
    "deadline": "31.12.2024"
}

# Генерация Word документа
generator.generate_word(
    "templates/contract_template.docx",
    data,
    "output/contract.docx"
)
```

### Генерация PDF

```python
pdf_data = {
    "title": "Финансовый отчет",
    "date": "20.12.2024",
    "content": "Содержание отчета...",
    "table_data": [
        ["Показатель", "Значение"],
        ["Выручка", "422000 руб."],
        ["Прибыль", "72000 руб."]
    ]
}

generator.generate_pdf(None, pdf_data, "output/report.pdf")
```

### Генерация Excel

```python
excel_data = {
    "title": "Финансовый отчет",
    "table_data": [
        ["Месяц", "Выручка", "Расходы"],
        ["Январь", "35000", "28000"],
        ["Февраль", "38000", "30000"]
    ]
}

generator.generate_excel(None, excel_data, "output/report.xlsx")
```

### Использование конфигурационного файла

Создайте JSON файл с конфигурацией:

```json
{
  "documents": [
    {
      "type": "word",
      "template": "templates/contract_template.docx",
      "output": "output/contract.docx",
      "data": {
        "contract_number": "ДГ-2024-001",
        "date": "20.12.2024"
      }
    }
  ]
}
```

Запустите генерацию:

```python
generator.generate_from_config("config/generation_config.json")
```

### Использование из командной строки

```bash
# Генерация из конфигурационного файла
python main.py --config config/generation_config.json

# Генерация одного документа
python main.py --type word --data data/sample_data.json --template templates/contract_template.docx --output output/contract.docx
```

## Формат шаблонов

### Word шаблоны

Используйте переменные в формате `{{variable_name}}`:

```
ДОГОВОР № {{contract_number}}

Дата: {{date}}

{{party1_name}} и {{party2_name}} заключили договор...
```

### Данные для документов

Данные передаются в виде словаря Python:

```python
{
    "variable_name": "значение",
    "number": 123,
    "date": "20.12.2024"
}
```

## Примеры

### Пример 1: Генерация договора

См. `examples/basic_example.py`

### Пример 2: Использование конфигурации

См. `examples/config_example.py`

## API Reference

### DocumentGenerator

#### Методы

- `generate_word(template_path, data, output_path)` - генерация Word документа
- `generate_pdf(template_path, data, output_path)` - генерация PDF документа
- `generate_excel(template_path, data, output_path)` - генерация Excel документа
- `generate_from_config(config_path)` - генерация из конфигурационного файла

### WordGenerator

- `generate(template_path, data, output_path)` - генерация Word документа
- `create_from_scratch(data, output_path)` - создание документа с нуля

### PDFGenerator

- `generate(template_path, data, output_path)` - генерация PDF документа
- `generate_from_template(template_path, data, output_path)` - генерация из HTML шаблона

### ExcelGenerator

- `generate(template_path, data, output_path)` - генерация Excel документа
- `create_report(data, output_path)` - создание финансового отчета

## Расширение функциональности

### Добавление нового типа документа

1. Создайте новый генератор в `doc_generator/`
2. Добавьте метод в `DocumentGenerator`
3. Обновите конфигурацию

### Добавление новых шаблонов

1. Создайте шаблон в `templates/`
2. Используйте переменные в формате `{{variable_name}}`
3. Добавьте пример использования в `examples/`

## Технические детали

### Используемые библиотеки

- `python-docx` - работа с Word документами
- `openpyxl` - работа с Excel файлами
- `fpdf2` - генерация PDF
- `jinja2` - шаблонизация (для будущего расширения)

### Поддержка форматов

- **Word**: .docx (чтение и запись)
- **PDF**: .pdf (генерация)
- **Excel**: .xlsx (чтение и запись)

## Ограничения

1. PDF генератор использует базовые шрифты (без кириллицы по умолчанию)
2. HTML шаблоны для PDF требуют дополнительной настройки
3. Сложное форматирование Word требует ручной настройки шаблонов

## Планы развития

- [ ] Поддержка кириллицы в PDF
- [ ] Генерация из HTML шаблонов в PDF
- [ ] Поддержка изображений в документах
- [ ] Веб-интерфейс для генерации
- [ ] Интеграция с базами данных
- [ ] Поддержка электронной подписи

## Автор

Разработано в рамках производственной практики  
ООО "Система Связи"

## Лицензия

Проект создан в образовательных целях.

