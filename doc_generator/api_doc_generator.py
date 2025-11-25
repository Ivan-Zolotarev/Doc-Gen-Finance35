"""
Генератор API документации
"""

import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
from .code_analyzer import CodeAnalyzer


class APIDocGenerator:
    """Генератор документации для API"""
    
    def __init__(self):
        """Инициализация генератора"""
        self.analyzer = CodeAnalyzer()
    
    def generate_from_flask_app(self, app_file: str) -> Dict[str, Any]:
        """
        Генерация документации из Flask приложения
        
        Args:
            app_file: Путь к файлу с Flask приложением
            
        Returns:
            Словарь с API документацией
        """
        code_info = self.analyzer.analyze_file(app_file)
        
        # Читаем исходный код для поиска маршрутов
        with open(app_file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        routes = self._extract_flask_routes(source)
        
        return {
            'title': 'API Documentation',
            'version': '1.0.0',
            'base_url': '/api',
            'routes': routes,
            'info': code_info
        }
    
    def _extract_flask_routes(self, source: str) -> List[Dict[str, Any]]:
        """Извлечение маршрутов Flask из исходного кода"""
        routes = []
        
        # Паттерн для поиска декораторов @app.route
        route_pattern = r'@app\.route\(["\']([^"\']+)["\'](?:\s*,\s*methods=\[([^\]]+)\])?\)'
        
        matches = re.finditer(route_pattern, source)
        
        for match in matches:
            path = match.group(1)
            methods_str = match.group(2) if match.group(2) else "'GET'"
            methods = [m.strip().strip("'\"") for m in methods_str.split(',')]
            
            # Ищем функцию после декоратора
            func_match = re.search(
                r'def\s+(\w+)\s*\([^)]*\)\s*:',
                source[match.end():match.end()+500]
            )
            
            if func_match:
                func_name = func_match.group(1)
                # Извлекаем docstring функции
                docstring_match = re.search(
                    r'"""(.*?)"""',
                    source[match.end():match.end()+1000],
                    re.DOTALL
                )
                
                docstring = docstring_match.group(1).strip() if docstring_match else ''
                
                # Извлекаем параметры из пути
                path_params = re.findall(r'<(\w+)(?::([^>]+))?>', path)
                
                route_info = {
                    'path': path,
                    'methods': methods,
                    'function': func_name,
                    'description': docstring,
                    'parameters': [
                        {
                            'name': param[0] if len(param) > 0 else 'unknown',
                            'type': param[1] if len(param) > 1 and param[1] else 'string',
                            'in': 'path',
                            'required': True
                        }
                        for param in path_params if len(param) > 0
                    ]
                }
                
                routes.append(route_info)
        
        return routes
    
    def generate_openapi_spec(self, api_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерация OpenAPI спецификации
        
        Args:
            api_info: Информация об API
            
        Returns:
            OpenAPI спецификация
        """
        spec = {
            'openapi': '3.0.0',
            'info': {
                'title': api_info.get('title', 'API'),
                'version': api_info.get('version', '1.0.0'),
                'description': api_info.get('description', '')
            },
            'servers': [
                {
                    'url': api_info.get('base_url', '/api'),
                    'description': 'API Server'
                }
            ],
            'paths': {}
        }
        
        for route in api_info.get('routes', []):
            path = route['path']
            methods = route.get('methods', ['GET'])
            
            if path not in spec['paths']:
                spec['paths'][path] = {}
            
            for method in methods:
                method_lower = method.lower()
                spec['paths'][path][method_lower] = {
                    'summary': route.get('description', ''),
                    'operationId': route.get('function', ''),
                    'parameters': route.get('parameters', []),
                    'responses': {
                        '200': {
                            'description': 'Successful response',
                            'content': {
                                'application/json': {
                                    'schema': {'type': 'object'}
                                }
                            }
                        }
                    }
                }
        
        return spec
    
    def generate_markdown(self, api_info: Dict[str, Any]) -> str:
        """
        Генерация Markdown документации
        
        Args:
            api_info: Информация об API
            
        Returns:
            Markdown строка
        """
        md = f"# {api_info.get('title', 'API Documentation')}\n\n"
        md += f"**Version:** {api_info.get('version', '1.0.0')}\n\n"
        md += f"**Base URL:** `{api_info.get('base_url', '/api')}`\n\n"
        
        md += "## Endpoints\n\n"
        
        for route in api_info.get('routes', []):
            methods_str = ', '.join(route.get('methods', ['GET']))
            md += f"### {methods_str} {route['path']}\n\n"
            
            if route.get('description'):
                md += f"{route['description']}\n\n"
            
            if route.get('parameters'):
                md += "**Parameters:**\n\n"
                md += "| Name | Type | Location | Required | Description |\n"
                md += "|------|------|----------|----------|-------------|\n"
                
                for param in route['parameters']:
                    md += f"| {param['name']} | {param.get('type', 'string')} | "
                    md += f"{param.get('in', 'path')} | {param.get('required', True)} | "
                    md += f"{param.get('description', '')} |\n"
                md += "\n"
            
            md += "---\n\n"
        
        return md

