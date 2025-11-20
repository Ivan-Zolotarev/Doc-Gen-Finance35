"""
Основной класс для генерации документов
"""

import os
from typing import Dict, Any, Optional
from .word_generator import WordGenerator
from .pdf_generator import PDFGenerator
from .excel_generator import ExcelGenerator


class DocumentGenerator:
    """Универсальный генератор документов"""
    
    def __init__(self, output_dir: str = "output"):
        """
        Инициализация генератора
        
        Args:
            output_dir: Директория для сохранения сгенерированных документов
        """
        self.output_dir = output_dir
        self.word_gen = WordGenerator()
        self.pdf_gen = PDFGenerator()
        self.excel_gen = ExcelGenerator()
        
        # Создаем директорию для выходных файлов
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_word(self, template_path: str, data: Dict[str, Any], 
                     output_path: Optional[str] = None) -> str:
        """
        Генерация Word документа
        
        Args:
            template_path: Путь к шаблону Word
            data: Данные для заполнения
            output_path: Путь для сохранения (если None, генерируется автоматически)
            
        Returns:
            Путь к сгенерированному файлу
        """
        if output_path is None:
            filename = os.path.basename(template_path).replace('.docx', '_generated.docx')
            output_path = os.path.join(self.output_dir, filename)
        
        return self.word_gen.generate(template_path, data, output_path)
    
    def generate_pdf(self, template_path: str, data: Dict[str, Any],
                    output_path: Optional[str] = None) -> str:
        """
        Генерация PDF документа
        
        Args:
            template_path: Путь к шаблону (HTML или текстовый)
            data: Данные для заполнения
            output_path: Путь для сохранения
            
        Returns:
            Путь к сгенерированному файлу
        """
        if output_path is None:
            filename = os.path.basename(template_path).replace('.html', '_generated.pdf')
            output_path = os.path.join(self.output_dir, filename)
        
        return self.pdf_gen.generate(template_path, data, output_path)
    
    def generate_excel(self, template_path: Optional[str], data: Dict[str, Any],
                      output_path: Optional[str] = None) -> str:
        """
        Генерация Excel документа
        
        Args:
            template_path: Путь к шаблону Excel (опционально)
            data: Данные для заполнения
            output_path: Путь для сохранения
            
        Returns:
            Путь к сгенерированному файлу
        """
        if output_path is None:
            output_path = os.path.join(self.output_dir, "report_generated.xlsx")
        
        return self.excel_gen.generate(template_path, data, output_path)
    
    def generate_from_config(self, config_path: str) -> list:
        """
        Генерация документов на основе конфигурационного файла
        
        Args:
            config_path: Путь к JSON конфигурационному файлу
            
        Returns:
            Список путей к сгенерированным файлам
        """
        import json
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        generated_files = []
        
        for doc_config in config.get('documents', []):
            doc_type = doc_config.get('type')
            template = doc_config.get('template')
            data = doc_config.get('data', {})
            output = doc_config.get('output')
            
            if doc_type == 'word':
                file_path = self.generate_word(template, data, output)
            elif doc_type == 'pdf':
                file_path = self.generate_pdf(template, data, output)
            elif doc_type == 'excel':
                file_path = self.generate_excel(template, data, output)
            else:
                raise ValueError(f"Неизвестный тип документа: {doc_type}")
            
            generated_files.append(file_path)
        
        return generated_files

