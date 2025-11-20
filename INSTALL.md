# Инструкция по установке и запуску

## Шаг 1: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 2: Создание шаблонов

Запустите скрипт для создания шаблонов документов:

```bash
python templates/create_templates.py
```

Это создаст необходимые шаблоны в директории `templates/`.

## Шаг 3: Запуск примеров

### Базовый пример

```bash
python examples/basic_example.py
```

Это создаст примеры документов в директории `output/`.

### Пример с конфигурацией

```bash
python examples/config_example.py
```

## Шаг 4: Использование из командной строки

### Генерация из конфигурационного файла

```bash
python main.py --config config/generation_config.json
```

### Генерация одного документа

```bash
python main.py --type word --data data/sample_data.json --template templates/contract_template.docx --output output/contract.docx
```

## Проверка работы

После выполнения примеров проверьте директорию `output/` - там должны появиться сгенерированные документы:
- `contract_generated.docx` - договор в формате Word
- `report_generated.pdf` - отчет в формате PDF
- `report_generated.xlsx` - отчет в формате Excel

## Решение проблем

### Ошибка импорта модулей

Убедитесь, что вы находитесь в корневой директории проекта и все зависимости установлены:

```bash
pip install -r requirements.txt
```

### Ошибка при создании шаблонов

Убедитесь, что директория `templates/` существует и доступна для записи.

### Ошибка при генерации PDF с кириллицей

Текущая версия использует базовые шрифты. Для поддержки кириллицы необходимо добавить TTF шрифты в код генератора PDF.

