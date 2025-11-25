"""
Генератор документации для баз данных
"""

import re
from typing import Dict, List, Any, Optional
from sqlalchemy import inspect, create_engine, MetaData, Table
from sqlalchemy.engine import Engine


class DBDocGenerator:
    """Генератор документации для баз данных"""
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Инициализация генератора
        
        Args:
            connection_string: Строка подключения к БД (опционально)
        """
        self.connection_string = connection_string
        self.engine = None
        if connection_string:
            self.engine = create_engine(connection_string)
    
    def analyze_database(self, connection_string: str) -> Dict[str, Any]:
        """
        Анализ структуры базы данных
        
        Args:
            connection_string: Строка подключения
            
        Returns:
            Словарь с информацией о БД
        """
        engine = create_engine(connection_string)
        inspector = inspect(engine)
        
        db_info = {
            'database': inspector.bind.url.database,
            'tables': []
        }
        
        for table_name in inspector.get_table_names():
            table_info = self._analyze_table(inspector, table_name)
            db_info['tables'].append(table_info)
        
        return db_info
    
    def _analyze_table(self, inspector, table_name: str) -> Dict[str, Any]:
        """Анализ таблицы"""
        columns = inspector.get_columns(table_name)
        primary_keys = inspector.get_primary_key_constraint(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)
        indexes = inspector.get_indexes(table_name)
        
        return {
            'name': table_name,
            'columns': [
                {
                    'name': col['name'],
                    'type': str(col['type']),
                    'nullable': col.get('nullable', True),
                    'default': str(col.get('default', '')),
                    'primary_key': col['name'] in primary_keys.get('constrained_columns', [])
                }
                for col in columns
            ],
            'primary_keys': primary_keys.get('constrained_columns', []),
            'foreign_keys': [
                {
                    'name': fk['name'],
                    'constrained_columns': fk['constrained_columns'],
                    'referred_table': fk['referred_table'],
                    'referred_columns': fk['referred_columns']
                }
                for fk in foreign_keys
            ],
            'indexes': [
                {
                    'name': idx['name'],
                    'columns': idx['column_names'],
                    'unique': idx.get('unique', False)
                }
                for idx in indexes
            ]
        }
    
    def generate_er_diagram_mermaid(self, db_info: Dict[str, Any]) -> str:
        """
        Генерация ER-диаграммы в формате Mermaid
        
        Args:
            db_info: Информация о БД
            
        Returns:
            Mermaid диаграмма
        """
        mermaid = "erDiagram\n"
        
        # Определяем связи
        relationships = []
        
        for table in db_info['tables']:
            table_name = table['name']
            mermaid += f"    {table_name} {{\n"
            
            for col in table['columns']:
                col_type = self._simplify_type(col['type'])
                pk_marker = " PK" if col['primary_key'] else ""
                mermaid += f"        {col_type} {col['name']}{pk_marker}\n"
            
            mermaid += "    }\n\n"
            
            # Собираем связи
            for fk in table['foreign_keys']:
                relationships.append({
                    'from': table_name,
                    'to': fk['referred_table'],
                    'from_col': fk['constrained_columns'][0] if fk['constrained_columns'] else '',
                    'to_col': fk['referred_columns'][0] if fk['referred_columns'] else ''
                })
        
        # Добавляем связи
        for rel in relationships:
            mermaid += f"    {rel['from']} ||--o{{ {rel['to']} : \"{rel['from_col']} -> {rel['to_col']}\"\n"
        
        return mermaid
    
    def _simplify_type(self, db_type: str) -> str:
        """Упрощение типа данных для диаграммы"""
        type_lower = db_type.lower()
        
        if 'int' in type_lower:
            return 'int'
        elif 'varchar' in type_lower or 'text' in type_lower or 'char' in type_lower:
            return 'string'
        elif 'date' in type_lower or 'time' in type_lower:
            return 'date'
        elif 'decimal' in type_lower or 'float' in type_lower or 'double' in type_lower:
            return 'float'
        elif 'bool' in type_lower:
            return 'boolean'
        else:
            return 'string'
    
    def generate_markdown(self, db_info: Dict[str, Any]) -> str:
        """
        Генерация Markdown документации
        
        Args:
            db_info: Информация о БД
            
        Returns:
            Markdown строка
        """
        md = f"# Database Documentation: {db_info.get('database', 'Unknown')}\n\n"
        md += f"## Tables ({len(db_info.get('tables', []))})\n\n"
        
        for table in db_info.get('tables', []):
            md += f"### {table['name']}\n\n"
            
            # Описание таблицы
            md += "**Columns:**\n\n"
            md += "| Column | Type | Nullable | Primary Key | Default |\n"
            md += "|--------|------|----------|-------------|----------|\n"
            
            for col in table['columns']:
                md += f"| {col['name']} | {col['type']} | "
                md += f"{'Yes' if col['nullable'] else 'No'} | "
                md += f"{'Yes' if col['primary_key'] else 'No'} | "
                md += f"{col.get('default', '')} |\n"
            
            md += "\n"
            
            # Внешние ключи
            if table.get('foreign_keys'):
                md += "**Foreign Keys:**\n\n"
                for fk in table['foreign_keys']:
                    md += f"- `{fk['name']}`: "
                    md += f"{', '.join(fk['constrained_columns'])} -> "
                    md += f"{fk['referred_table']}({', '.join(fk['referred_columns'])})\n"
                md += "\n"
            
            md += "---\n\n"
        
        return md
    
    def analyze_sql_file(self, sql_file: str) -> Dict[str, Any]:
        """
        Анализ SQL файла
        
        Args:
            sql_file: Путь к SQL файлу
            
        Returns:
            Информация о структуре БД из SQL
        """
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        tables = []
        
        # Поиск CREATE TABLE
        create_table_pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?\s*\((.*?)\)'
        
        matches = re.finditer(create_table_pattern, sql_content, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            table_name = match.group(1)
            table_body = match.group(2)
            
            columns = self._parse_table_columns(table_body)
            primary_keys = self._extract_primary_keys(table_body)
            foreign_keys = self._extract_foreign_keys(table_body)
            
            tables.append({
                'name': table_name,
                'columns': columns,
                'primary_keys': primary_keys,
                'foreign_keys': foreign_keys
            })
        
        return {
            'database': 'from_sql_file',
            'tables': tables
        }
    
    def _parse_table_columns(self, table_body: str) -> List[Dict[str, Any]]:
        """Парсинг колонок из SQL"""
        columns = []
        lines = table_body.split(',')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('PRIMARY') or line.startswith('FOREIGN') or line.startswith('UNIQUE'):
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                col_name = parts[0].strip('`')
                col_type = parts[1] if len(parts) > 1 else 'TEXT'
                nullable = 'NOT NULL' not in line.upper()
                default = None
                
                if 'DEFAULT' in line.upper():
                    default_match = re.search(r'DEFAULT\s+([^\s,]+)', line, re.IGNORECASE)
                    if default_match:
                        default = default_match.group(1)
                
                columns.append({
                    'name': col_name,
                    'type': col_type,
                    'nullable': nullable,
                    'default': default,
                    'primary_key': False
                })
        
        return columns
    
    def _extract_primary_keys(self, table_body: str) -> List[str]:
        """Извлечение первичных ключей"""
        pk_match = re.search(r'PRIMARY\s+KEY\s*\(([^)]+)\)', table_body, re.IGNORECASE)
        if pk_match:
            keys = [k.strip().strip('`') for k in pk_match.group(1).split(',')]
            return keys
        return []
    
    def _extract_foreign_keys(self, table_body: str) -> List[Dict[str, Any]]:
        """Извлечение внешних ключей"""
        fks = []
        fk_pattern = r'FOREIGN\s+KEY\s*\(([^)]+)\)\s+REFERENCES\s+(\w+)\s*\(([^)]+)\)'
        
        matches = re.finditer(fk_pattern, table_body, re.IGNORECASE)
        
        for match in matches:
            fks.append({
                'constrained_columns': [c.strip().strip('`') for c in match.group(1).split(',')],
                'referred_table': match.group(2),
                'referred_columns': [c.strip().strip('`') for c in match.group(3).split(',')]
            })
        
        return fks

