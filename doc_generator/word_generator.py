"""
Генератор Word документов
"""

import os
from typing import Dict, Any
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re


class WordGenerator:
    """Генератор документов в формате Word (.docx)"""
    
    def generate(self, template_path: str, data: Dict[str, Any], output_path: str) -> str:
        """
        Генерация Word документа из шаблона
        
        Args:
            template_path: Путь к шаблону Word
            data: Словарь с данными для подстановки
            output_path: Путь для сохранения результата
            
        Returns:
            Путь к сгенерированному файлу
        """
        if not os.path.exists(template_path):
            # Создаем новый документ, если шаблон не существует
            doc = Document()
            doc.add_heading('Документ', 0)
            doc.add_paragraph('{{content}}')
        else:
            doc = Document(template_path)
        
        # Заменяем переменные в документе
        self._replace_variables(doc, data)
        
        # Сохраняем документ
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        doc.save(output_path)
        
        return output_path
    
    def _replace_variables(self, doc: Document, data: Dict[str, Any]):
        """
        Замена переменных в документе
        
        Args:
            doc: Объект документа Word
            data: Словарь с данными
        """
        # Обрабатываем параграфы
        for paragraph in doc.paragraphs:
            self._replace_in_paragraph(paragraph, data)
        
        # Обрабатываем таблицы
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        self._replace_in_paragraph(paragraph, data)
    
    def _replace_in_paragraph(self, paragraph, data: Dict[str, Any]):
        """
        Замена переменных в параграфе
        
        Args:
            paragraph: Параграф документа
            data: Словарь с данными
        """
        text = paragraph.text
        
        # Ищем все переменные в формате {{variable_name}}
        pattern = r'\{\{(\w+)\}\}'
        matches = re.findall(pattern, text)
        
        if matches:
            # Сохраняем форматирование
            runs = paragraph.runs
            paragraph.clear()
            
            # Разбиваем текст на части и заменяем переменные
            parts = re.split(pattern, text)
            
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    # Обычный текст
                    if part:
                        paragraph.add_run(part)
                else:
                    # Переменная
                    var_name = part
                    value = str(data.get(var_name, f'{{{{{var_name}}}}}'))
                    run = paragraph.add_run(value)
                    # Применяем базовое форматирование
                    if runs:
                        run.font.size = runs[0].font.size if runs[0].font.size else Pt(11)
    
    def create_from_scratch(self, data: Dict[str, Any], output_path: str) -> str:
        """
        Создание Word документа с нуля
        
        Args:
            data: Данные для документа
            output_path: Путь для сохранения
            
        Returns:
            Путь к созданному файлу
        """
        doc = Document()
        
        # Заголовок
        if 'title' in data:
            doc.add_heading(data['title'], 0)
        
        # Содержание
        if 'content' in data:
            if isinstance(data['content'], list):
                for item in data['content']:
                    doc.add_paragraph(item, style='List Bullet')
            else:
                doc.add_paragraph(str(data['content']))
        
        # Таблица, если есть
        if 'table_data' in data:
            table = doc.add_table(rows=1, cols=len(data['table_data'][0]))
            table.style = 'Light Grid Accent 1'
            
            # Заголовки
            header_cells = table.rows[0].cells
            for i, header in enumerate(data['table_data'][0]):
                header_cells[i].text = str(header)
            
            # Данные
            for row_data in data['table_data'][1:]:
                row_cells = table.add_row().cells
                for i, cell_data in enumerate(row_data):
                    row_cells[i].text = str(cell_data)
        
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        doc.save(output_path)
        
        return output_path

