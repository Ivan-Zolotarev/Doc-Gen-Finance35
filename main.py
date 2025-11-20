"""
Главный файл для запуска генератора документов
"""

import sys
import argparse
from doc_generator import DocumentGenerator
import json
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='Генератор документов Doc-Gen-Finance35')
    parser.add_argument('--config', '-c', type=str, help='Путь к конфигурационному файлу JSON')
    parser.add_argument('--type', '-t', type=str, choices=['word', 'pdf', 'excel'], 
                       help='Тип документа для генерации')
    parser.add_argument('--template', type=str, help='Путь к шаблону')
    parser.add_argument('--data', '-d', type=str, help='Путь к файлу с данными (JSON)')
    parser.add_argument('--output', '-o', type=str, help='Путь для сохранения результата')
    
    args = parser.parse_args()
    
    generator = DocumentGenerator()
    
    if args.config:
        # Генерация из конфигурационного файла
        print(f"Загрузка конфигурации из {args.config}...")
        generated_files = generator.generate_from_config(args.config)
        print(f"\nСгенерировано {len(generated_files)} документов:")
        for file_path in generated_files:
            print(f"  - {file_path}")
    elif args.type and args.data:
        # Генерация одного документа
        with open(args.data, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        output = args.output or f"output/document_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if args.type == 'word':
            template = args.template or "templates/contract_template.docx"
            output += ".docx"
            file_path = generator.generate_word(template, data, output)
        elif args.type == 'pdf':
            template = args.template
            output += ".pdf"
            file_path = generator.generate_pdf(template, data, output)
        elif args.type == 'excel':
            template = args.template
            output += ".xlsx"
            file_path = generator.generate_excel(template, data, output)
        
        print(f"Документ создан: {file_path}")
    else:
        parser.print_help()
        print("\nПримеры использования:")
        print("  python main.py --config config/generation_config.json")
        print("  python main.py --type word --data data/sample_data.json --template templates/contract_template.docx")
        sys.exit(1)


if __name__ == "__main__":
    main()

