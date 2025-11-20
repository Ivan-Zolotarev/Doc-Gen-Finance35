"""
Базовый пример использования генератора документов
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в путь
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from doc_generator import DocumentGenerator
from datetime import datetime

def main():
    # Инициализация генератора
    generator = DocumentGenerator(output_dir="output")
    
    # Пример данных для договора
    contract_data = {
        "contract_number": "ДГ-2024-001",
        "date": datetime.now().strftime("%d.%m.%Y"),
        "party1_name": "ООО 'Система Связи'",
        "party2_name": "ООО 'Клиент'",
        "subject": "Разработка программного обеспечения для автоматической генерации документации",
        "amount": "500 000",
        "deadline": "31.12.2024",
        "customer_signature": "Иванов И.И.",
        "executor_signature": "Веселенко Т.Н."
    }
    
    # Генерация Word документа
    print("Генерация договора...")
    word_file = generator.generate_word(
        "templates/contract_template.docx",
        contract_data,
        "output/contract_generated.docx"
    )
    print(f"Договор создан: {word_file}")
    
    # Пример данных для финансового отчета
    report_data = {
        "title": "Финансовый отчет",
        "company_name": "ООО 'Система Связи'",
        "inn": "7100053584",
        "ogrn": "1247100004942",
        "date": datetime.now().strftime("%d.%m.%Y"),
        "period_start": "01.01.2024",
        "period_end": "31.12.2024",
        "revenue": "422 000",
        "expenses": "350 000",
        "profit": "72 000",
        "content": "Отчет о финансовой деятельности организации за 2024 год.",
        "table_data": [
            ["Показатель", "Значение", "Единица"],
            ["Выручка", "422 000", "руб."],
            ["Расходы", "350 000", "руб."],
            ["Прибыль", "72 000", "руб."]
        ],
        "signature": "Веселенко Т.Н."
    }
    
    # Генерация PDF документа
    print("\nГенерация PDF отчета...")
    pdf_file = generator.generate_pdf(
        None,
        report_data,
        "output/report_generated.pdf"
    )
    print(f"PDF отчет создан: {pdf_file}")
    
    # Генерация Excel отчета
    print("\nГенерация Excel отчета...")
    excel_data = {
        "title": "Финансовый отчет за 2024 год",
        "sheet_name": "Отчет",
        "table_data": [
            ["Показатель", "Январь", "Февраль", "Март", "Итого"],
            ["Выручка", "35000", "38000", "42000", "115000"],
            ["Расходы", "28000", "30000", "32000", "90000"],
            ["Прибыль", "7000", "8000", "10000", "25000"]
        ],
        "additional_data": {
            "Средняя выручка": "38333 руб.",
            "Средние расходы": "30000 руб.",
            "Средняя прибыль": "8333 руб."
        }
    }
    
    excel_file = generator.generate_excel(
        None,
        excel_data,
        "output/report_generated.xlsx"
    )
    print(f"Excel отчет создан: {excel_file}")
    
    print("\nВсе документы успешно сгенерированы!")

if __name__ == "__main__":
    main()

