"""
Генератор Markdown документации
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
from .code_analyzer import CodeAnalyzer


class MarkdownGenerator:
    """Генератор документации в формате Markdown"""
    
    def __init__(self):
        """Инициализация генератора"""
        self.analyzer = CodeAnalyzer()
    
    def generate_code_docs(self, code_info: Dict[str, Any], 
                          output_path: Optional[str] = None) -> str:
        """
        Генерация документации из анализа кода
        
        Args:
            code_info: Информация о коде из CodeAnalyzer
            output_path: Путь для сохранения (опционально)
            
        Returns:
            Markdown строка
        """
        # Проверяем наличие ошибки
        if 'error' in code_info:
            return f"*Ошибка при анализе: {code_info['error']}*\n\n"
        
        md = "# Code Documentation\n\n"
        
        if code_info.get('file'):
            md += f"**File:** `{code_info['file']}`\n\n"
        
        if code_info.get('module_docstring'):
            md += f"{code_info['module_docstring']}\n\n"
        
        md += f"**Lines of code:** {code_info.get('line_count', 0)}\n\n"
        
        # Импорты
        if code_info.get('imports'):
            md += "## Imports\n\n"
            for imp in code_info['imports']:
                if imp.get('type') == 'import':
                    md += f"- `import {', '.join(imp['names'])}`\n"
                elif imp.get('type') == 'from':
                    md += f"- `from {imp['module']} import {', '.join(imp['names'])}`\n"
            md += "\n"
        
        # Классы
        if code_info.get('classes'):
            md += "## Classes\n\n"
            for cls in code_info['classes']:
                md += self._generate_class_doc(cls)
                md += "\n"
        
        # Функции
        if code_info.get('functions'):
            md += "## Functions\n\n"
            for func in code_info['functions']:
                md += self._generate_function_doc(func)
                md += "\n"
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md)
        
        return md
    
    def _generate_class_doc(self, cls: Dict[str, Any]) -> str:
        """Генерация документации для класса"""
        md = f"### {cls['name']}\n\n"
        
        if cls.get('docstring'):
            md += f"{cls['docstring']}\n\n"
        
        if cls.get('bases'):
            md += f"**Inherits from:** {', '.join(cls['bases'])}\n\n"
        
        if cls.get('decorators'):
            md += f"**Decorators:** {', '.join(cls['decorators'])}\n\n"
        
        if cls.get('attributes'):
            md += "**Attributes:**\n\n"
            for attr in cls['attributes']:
                md += f"- `{attr}`\n"
            md += "\n"
        
        if cls.get('methods'):
            md += "**Methods:**\n\n"
            for method in cls['methods']:
                md += f"- `{method['name']}({', '.join([arg['name'] for arg in method.get('args', [])])})`\n"
            md += "\n"
        
        return md
    
    def _generate_function_doc(self, func: Dict[str, Any]) -> str:
        """Генерация документации для функции"""
        md = f"### {func['name']}\n\n"
        
        if func.get('docstring'):
            doc_sections = self.analyzer.extract_docstring_sections(func['docstring'])
            
            if doc_sections.get('description'):
                md += f"{doc_sections['description']}\n\n"
            
            if func.get('args'):
                md += "**Parameters:**\n\n"
                md += "| Name | Type | Default | Description |\n"
                md += "|------|------|---------|-------------|\n"
                
                for arg in func['args']:
                    arg_name = arg['name']
                    arg_type = arg.get('annotation', 'Any')
                    arg_default = arg.get('default', '')
                    arg_desc = doc_sections.get('args', {}).get(arg_name, '')
                    
                    md += f"| {arg_name} | {arg_type} | {arg_default} | {arg_desc} |\n"
                md += "\n"
            
            if func.get('returns'):
                md += f"**Returns:** `{func['returns']}`\n\n"
                if doc_sections.get('returns'):
                    md += f"{doc_sections['returns']}\n\n"
            
            if doc_sections.get('raises'):
                md += "**Raises:**\n\n"
                for exc, desc in doc_sections['raises'].items():
                    md += f"- `{exc}`: {desc}\n"
                md += "\n"
            
            if doc_sections.get('examples'):
                md += "**Example:**\n\n```python\n"
                md += f"{doc_sections['examples']}\n"
                md += "```\n\n"
        else:
            # Без docstring, просто сигнатура
            args_str = ', '.join([arg['name'] for arg in func.get('args', [])])
            md += f"```python\ndef {func['name']}({args_str})"
            if func.get('returns'):
                md += f" -> {func['returns']}"
            md += ":\n    ...\n```\n\n"
        
        return md
    
    def generate_project_docs(self, directory: str, output_path: Optional[str] = None) -> str:
        """
        Генерация документации для всего проекта
        
        Args:
            directory: Путь к директории проекта
            output_path: Путь для сохранения
            
        Returns:
            Markdown строка
        """
        analysis = self.analyzer.analyze_directory(directory)
        
        md = "# Project Documentation\n\n"
        md += f"**Directory:** `{analysis.get('directory', directory)}`\n\n"
        
        summary = analysis.get('summary', {})
        md += f"**Summary:**\n"
        md += f"- Total files: {summary.get('total_files', 0)}\n"
        md += f"- Total classes: {summary.get('total_classes', 0)}\n"
        md += f"- Total functions: {summary.get('total_functions', 0)}\n"
        md += f"- Total lines: {summary.get('total_lines', 0)}\n\n"
        
        md += "---\n\n"
        
        files = analysis.get('files', [])
        if not files:
            md += "*Файлы не найдены или не удалось проанализировать*\n\n"
        else:
            for file_info in files:
                try:
                    if 'error' in file_info:
                        md += f"## {file_info.get('file', 'unknown')}\n\n"
                        md += f"*Ошибка при анализе: {file_info.get('error', 'Unknown error')}*\n\n"
                        md += "---\n\n"
                        continue
                    
                    if not file_info.get('file'):
                        continue
                    
                    md += f"## {file_info['file']}\n\n"
                    md += self.generate_code_docs(file_info)
                    md += "\n---\n\n"
                except Exception as e:
                    md += f"## {file_info.get('file', 'unknown')}\n\n"
                    md += f"*Ошибка при генерации документации: {str(e)}*\n\n"
                    md += "---\n\n"
                    continue
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md)
        
        return md

