"""
Doc-Gen-Finance35 - Система автоматической генерации документации
"""

from .generator import DocumentGenerator
from .word_generator import WordGenerator
from .pdf_generator import PDFGenerator
from .excel_generator import ExcelGenerator

__version__ = "1.0.0"
__all__ = ['DocumentGenerator', 'WordGenerator', 'PDFGenerator', 'ExcelGenerator']

