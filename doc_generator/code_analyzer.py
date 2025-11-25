"""
Анализатор кода для генерации технической документации
"""

import ast
import inspect
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
import re

try:
    from ast import unparse
except ImportError:
    try:
        from astunparse import unparse
    except ImportError:
        def unparse(node):
            """Fallback для unparse"""
            return str(node)


class CodeAnalyzer:
    """Анализатор Python кода для извлечения структуры и документации"""
    
    def __init__(self):
        """Инициализация анализатора"""
        self.modules = []
        self.classes = []
        self.functions = []
        self.imports = []
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Анализ Python файла
        
        Args:
            file_path: Путь к Python файлу
            
        Returns:
            Словарь с информацией о коде
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        return self.analyze_source(source_code, file_path)
    
    def analyze_source(self, source_code: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Анализ исходного кода
        
        Args:
            source_code: Исходный код
            file_path: Путь к файлу (опционально)
            
        Returns:
            Словарь с информацией о коде
        """
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return {
                'error': f'Синтаксическая ошибка: {e}',
                'file': file_path
            }
        
        info = {
            'file': file_path or 'unknown',
            'classes': [],
            'functions': [],
            'imports': [],
            'module_docstring': ast.get_docstring(tree),
            'line_count': len(source_code.split('\n'))
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = self._extract_class_info(node, source_code)
                info['classes'].append(class_info)
            
            elif isinstance(node, ast.FunctionDef):
                func_info = self._extract_function_info(node, source_code)
                info['functions'].append(func_info)
            
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                import_info = self._extract_import_info(node)
                info['imports'].append(import_info)
        
        return info
    
    def _extract_class_info(self, node: ast.ClassDef, source_code: str) -> Dict[str, Any]:
        """Извлечение информации о классе"""
        methods = []
        attributes = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._extract_function_info(item, source_code)
                methods.append(method_info)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)
        
        # Получаем базовые классы
        bases = [self._get_node_name(base) for base in node.bases]
        
        return {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'line_start': node.lineno,
            'line_end': node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
            'methods': methods,
            'attributes': attributes,
            'bases': bases,
            'decorators': [self._get_node_name(d) for d in node.decorator_list]
        }
    
    def _extract_function_info(self, node: ast.FunctionDef, source_code: str) -> Dict[str, Any]:
        """Извлечение информации о функции"""
        args = []
        
        # Обработка аргументов
        for arg in node.args.args:
            try:
                annotation = None
                if arg.annotation:
                    try:
                        annotation = unparse(arg.annotation)
                    except Exception:
                        annotation = str(arg.annotation)
                
                arg_info = {
                    'name': arg.arg,
                    'annotation': annotation
                }
                args.append(arg_info)
            except Exception as e:
                # Пропускаем проблемные аргументы
                print(f"Ошибка при обработке аргумента: {e}")
                continue
        
        # Обработка дефолтных значений
        defaults = node.args.defaults
        if defaults and len(defaults) > 0:
            for i, default in enumerate(defaults):
                idx = len(args) - len(defaults) + i
                if idx >= 0 and idx < len(args):
                    try:
                        args[idx]['default'] = unparse(default) if default else None
                    except Exception:
                        args[idx]['default'] = str(default) if default else None
        
        # Возвращаемое значение
        returns = None
        if node.returns:
            try:
                returns = unparse(node.returns)
            except Exception:
                returns = str(node.returns)
        
        return {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'args': args,
            'returns': returns,
            'line_start': node.lineno,
            'line_end': node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
            'decorators': [self._get_node_name(d) for d in node.decorator_list],
            'is_async': isinstance(node, ast.AsyncFunctionDef)
        }
    
    def _extract_import_info(self, node: ast.Import) -> Dict[str, Any]:
        """Извлечение информации об импортах"""
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
            return {'type': 'import', 'names': names}
        elif isinstance(node, ast.ImportFrom):
            names = [alias.name for alias in node.names]
            return {
                'type': 'from',
                'module': node.module,
                'names': names,
                'level': node.level
            }
        return {}
    
    def _get_node_name(self, node: ast.AST) -> str:
        """Получение имени узла AST"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_node_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_node_name(node.func)
        else:
            try:
                return unparse(node)
            except:
                return str(node)
    
    def analyze_directory(self, directory: str, extensions: List[str] = None) -> Dict[str, Any]:
        """
        Анализ директории с кодом
        
        Args:
            directory: Путь к директории
            extensions: Список расширений файлов (по умолчанию ['.py'])
            
        Returns:
            Словарь с информацией о всех файлах
        """
        if extensions is None:
            extensions = ['.py']
        
        results = {
            'directory': directory,
            'files': [],
            'summary': {
                'total_files': 0,
                'total_classes': 0,
                'total_functions': 0,
                'total_lines': 0
            }
        }
        
        path = Path(directory)
        if not path.exists():
            return results
        
        for file_path in path.rglob('*'):
            if file_path.suffix in extensions and file_path.is_file():
                try:
                    file_info = self.analyze_file(str(file_path))
                    results['files'].append(file_info)
                    
                    # Пропускаем файлы с ошибками при подсчете статистики
                    if 'error' not in file_info:
                        results['summary']['total_files'] += 1
                        results['summary']['total_classes'] += len(file_info.get('classes', []))
                        results['summary']['total_functions'] += len(file_info.get('functions', []))
                        results['summary']['total_lines'] += file_info.get('line_count', 0)
                except Exception as e:
                    # Добавляем информацию об ошибке
                    error_info = {
                        'file': str(file_path),
                        'error': f'Ошибка при анализе: {str(e)}'
                    }
                    results['files'].append(error_info)
        
        return results
    
    def extract_docstring_sections(self, docstring: Optional[str]) -> Dict[str, str]:
        """
        Извлечение секций из docstring (Google/NumPy стиль)
        
        Args:
            docstring: Docstring для анализа
            
        Returns:
            Словарь с секциями
        """
        if not docstring:
            return {}
        
        sections = {
            'description': '',
            'args': {},
            'returns': '',
            'raises': {},
            'examples': ''
        }
        
        lines = docstring.split('\n')
        current_section = 'description'
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            # Определяем секции
            if line.lower().startswith('args:'):
                if current_section == 'description':
                    sections['description'] = '\n'.join(current_content).strip()
                current_section = 'args'
                current_content = []
            elif line.lower().startswith('returns:'):
                if current_section == 'args':
                    sections['args'] = self._parse_args_section('\n'.join(current_content))
                current_section = 'returns'
                current_content = []
            elif line.lower().startswith('raises:'):
                if current_section == 'returns':
                    sections['returns'] = '\n'.join(current_content).strip()
                current_section = 'raises'
                current_content = []
            elif line.lower().startswith('example'):
                if current_section == 'raises':
                    sections['raises'] = self._parse_raises_section('\n'.join(current_content))
                current_section = 'examples'
                current_content = []
            else:
                current_content.append(line)
        
        # Сохраняем последнюю секцию
        if current_section == 'description':
            sections['description'] = '\n'.join(current_content).strip()
        elif current_section == 'returns':
            sections['returns'] = '\n'.join(current_content).strip()
        elif current_section == 'examples':
            sections['examples'] = '\n'.join(current_content).strip()
        
        return sections
    
    def _parse_args_section(self, content: str) -> Dict[str, str]:
        """Парсинг секции Args"""
        args = {}
        lines = content.split('\n')
        current_arg = None
        
        for line in lines:
            line = line.strip()
            if ':' in line:
                parts = line.split(':', 1)
                current_arg = parts[0].strip()
                args[current_arg] = parts[1].strip() if len(parts) > 1 else ''
            elif current_arg and line:
                args[current_arg] += ' ' + line
        
        return args
    
    def _parse_raises_section(self, content: str) -> Dict[str, str]:
        """Парсинг секции Raises"""
        return self._parse_args_section(content)  # Аналогично Args

