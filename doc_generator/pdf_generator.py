"""
Генератор PDF документов
"""

import os
from typing import Dict, Any, Optional
from fpdf import FPDF
from datetime import datetime
import re


class PDFGenerator:
    """Генератор документов в формате PDF"""
    
    def __init__(self):
        """Инициализация генератора PDF"""
        self.font_path = None  # Можно добавить поддержку кириллицы через ttf шрифты
    
    def generate(self, template_path: Optional[str], data: Dict[str, Any], output_path: str) -> str:
        """
        Генерация PDF документа
        
        Args:
            template_path: Путь к шаблону (опционально, для будущей поддержки HTML шаблонов)
            data: Данные для документа
            output_path: Путь для сохранения
            
        Returns:
            Путь к сгенерированному файлу
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Настройка шрифта (базовый, без кириллицы)
        # Для кириллицы нужно добавить ttf шрифт
        pdf.set_font("Arial", size=12)
        
        # Заголовок
        if 'title' in data:
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, str(data['title']), ln=True, align='C')
            pdf.ln(5)
        
        # Дата
        if 'date' in data:
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 5, f"Дата: {data['date']}", ln=True)
            pdf.ln(5)
        
        # Основное содержимое
        pdf.set_font("Arial", size=12)
        
        if 'content' in data:
            content = str(data['content'])
            # Простая обработка многострочного текста
            lines = content.split('\n')
            for line in lines:
                if line.strip():
                    pdf.cell(0, 7, line, ln=True)
                else:
                    pdf.ln(3)
        
        # Таблица
        if 'table_data' in data and data['table_data']:
            self._add_table(pdf, data['table_data'])
        
        # Подпись
        if 'signature' in data:
            pdf.ln(10)
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 5, f"Подпись: {data['signature']}", ln=True)
        
        # Сохранение
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        pdf.output(output_path)
        
        return output_path
    
    def _add_table(self, pdf: FPDF, table_data: list):
        """
        Добавление таблицы в PDF
        
        Args:
            pdf: Объект PDF
            table_data: Данные таблицы (список списков)
        """
        if not table_data:
            return
        
        pdf.ln(5)
        pdf.set_font("Arial", "B", 11)
        
        # Определяем ширину колонок
        num_cols = len(table_data[0])
        col_width = 190 / num_cols
        
        # Заголовки
        for header in table_data[0]:
            pdf.cell(col_width, 7, str(header), border=1, align='C')
        pdf.ln()
        
        # Данные
        pdf.set_font("Arial", size=10)
        for row in table_data[1:]:
            for cell in row:
                pdf.cell(col_width, 6, str(cell), border=1)
            pdf.ln()
    
    def generate_from_template(self, template_path: str, data: Dict[str, Any], output_path: str) -> str:
        """
        Генерация PDF из HTML шаблона (базовая реализация)
        
        Args:
            template_path: Путь к HTML шаблону
            data: Данные для подстановки
            output_path: Путь для сохранения
            
        Returns:
            Путь к сгенерированному файлу
        """
        # Читаем шаблон
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Заменяем переменные
        pattern = r'\{\{(\w+)\}\}'
        html_content = re.sub(pattern, lambda m: str(data.get(m.group(1), '')), template)
        
        # Для полноценной поддержки HTML нужна библиотека weasyprint или pdfkit
        # Здесь упрощенная версия - просто извлекаем текст
        # В реальном проекте лучше использовать weasyprint
        
        # Создаем PDF из данных
        return self.generate(None, data, output_path)

