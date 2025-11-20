"""
Пример использования генератора с конфигурационным файлом
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в путь
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from doc_generator import DocumentGenerator
import json
from datetime import datetime

def create_config_file():
    """Создание примера конфигурационного файла"""
    config = {
        "documents": [
            {
                "type": "word",
                "template": "templates/contract_template.docx",
                "output": "output/contract_from_config.docx",
                "data": {
                    "contract_number": "ДГ-2024-002",
                    "date": datetime.now().strftime("%d.%m.%Y"),
                    "party1_name": "ООО 'Система Связи'",
                    "party2_name": "ООО 'Партнер'",
                    "subject": "Оказание услуг по разработке ПО",
                    "amount": "300 000",
                    "deadline": "15.01.2025",
                    "customer_signature": "Петров П.П.",
                    "executor_signature": "Веселенко Т.Н."
                }
            },
            {
                "type": "pdf",
                "template": None,
                "output": "output/report_from_config.pdf",
                "data": {
                    "title": "Ежемесячный отчет",
                    "date": datetime.now().strftime("%d.%m.%Y"),
                    "content": "Отчет о выполненных работах за декабрь 2024 года.\n\nВыполнены следующие задачи:\n- Разработка модуля генерации Word документов\n- Разработка модуля генерации PDF документов\n- Создание шаблонов документов",
                    "table_data": [
                        ["Задача", "Статус", "Дата"],
                        ["Модуль Word", "Выполнено", "15.12.2024"],
                        ["Модуль PDF", "Выполнено", "18.12.2024"],
                        ["Шаблоны", "Выполнено", "20.12.2024"]
                    ],
                    "signature": "Веселенко Т.Н."
                }
            },
            {
                "type": "excel",
                "template": None,
                "output": "output/financial_report_from_config.xlsx",
                "data": {
                    "title": "Финансовый отчет за 2024 год",
                    "sheet_name": "Финансы",
                    "table_data": [
                        ["Месяц", "Выручка", "Расходы", "Прибыль"],
                        ["Январь", "35000", "28000", "7000"],
                        ["Февраль", "38000", "30000", "8000"],
                        ["Март", "42000", "32000", "10000"],
                        ["Апрель", "45000", "34000", "11000"],
                        ["Май", "48000", "36000", "12000"],
                        ["Итого", "208000", "160000", "48000"]
                    ]
                }
            }
        ]
    }
    
    with open("config/generation_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("Конфигурационный файл создан: config/generation_config.json")

def main():
    # Создаем конфигурационный файл
    create_config_file()
    
    # Инициализация генератора
    generator = DocumentGenerator(output_dir="output")
    
    # Генерация документов из конфигурации
    print("Генерация документов из конфигурационного файла...")
    generated_files = generator.generate_from_config("config/generation_config.json")
    
    print("\nСгенерированные файлы:")
    for file_path in generated_files:
        print(f"  - {file_path}")
    
    print("\nВсе документы успешно сгенерированы!")

if __name__ == "__main__":
    main()

