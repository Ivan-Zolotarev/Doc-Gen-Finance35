"""
Генератор диаграмм для документации
"""

from typing import Dict, List, Any, Optional
from .code_analyzer import CodeAnalyzer


class DiagramGenerator:
    """Генератор различных типов диаграмм"""
    
    def __init__(self):
        """Инициализация генератора"""
        self.analyzer = CodeAnalyzer()
    
    def generate_class_diagram_mermaid(self, code_info: Dict[str, Any]) -> str:
        """
        Генерация диаграммы классов в формате Mermaid
        
        Args:
            code_info: Информация о коде
            
        Returns:
            Mermaid диаграмма
        """
        mermaid = "classDiagram\n"
        
        classes = code_info.get('classes', [])
        if not classes:
            return mermaid + "    class Empty { }\n"
        
        for cls in classes:
            if not isinstance(cls, dict) or 'name' not in cls:
                continue
            class_name = cls.get('name', 'Unknown')
            
            # Добавляем атрибуты
            attributes = []
            for attr in cls.get('attributes', []):
                attributes.append(f"  +{attr}")
            
            # Добавляем методы
            methods = []
            for method in cls.get('methods', []):
                try:
                    method_name = method.get('name', 'unknown')
                    args_list = method.get('args', [])
                    args = ', '.join([arg.get('name', '') for arg in args_list if isinstance(arg, dict)])
                    methods.append(f"  +{method_name}({args})")
                except Exception:
                    # Пропускаем методы с ошибками
                    continue
            
            mermaid += f"    class {class_name} {{\n"
            if attributes:
                mermaid += "\n".join(attributes) + "\n"
            if methods:
                mermaid += "\n".join(methods) + "\n"
            mermaid += "    }\n\n"
            
            # Добавляем наследование
            for base in cls.get('bases', []):
                base_name = base.split('.')[-1]  # Убираем модуль, оставляем только имя класса
                mermaid += f"    {base_name} <|-- {class_name}\n"
        
        return mermaid
    
    def generate_flowchart_mermaid(self, functions: List[Dict[str, Any]], 
                                   connections: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Генерация блок-схемы в формате Mermaid
        
        Args:
            functions: Список функций
            connections: Список связей между функциями
            
        Returns:
            Mermaid диаграмма
        """
        mermaid = "flowchart TD\n"
        
        # Создаем узлы для функций
        for func in functions:
            func_name = func['name']
            func_id = func_name.replace(' ', '_').replace('-', '_')
            mermaid += f"    {func_id}[\"{func_name}\"]\n"
        
        # Добавляем связи
        if connections:
            for conn in connections:
                from_id = conn['from'].replace(' ', '_').replace('-', '_')
                to_id = conn['to'].replace(' ', '_').replace('-', '_')
                mermaid += f"    {from_id} --> {to_id}\n"
        
        return mermaid
    
    def generate_sequence_diagram_mermaid(self, interactions: List[Dict[str, Any]]) -> str:
        """
        Генерация диаграммы последовательности в формате Mermaid
        
        Args:
            interactions: Список взаимодействий
            
        Returns:
            Mermaid диаграмма
        """
        mermaid = "sequenceDiagram\n"
        
        participants = set()
        for interaction in interactions:
            participants.add(interaction.get('from', ''))
            participants.add(interaction.get('to', ''))
        
        for participant in participants:
            if participant:
                mermaid += f"    participant {participant}\n"
        
        mermaid += "\n"
        
        for interaction in interactions:
            from_obj = interaction.get('from', '')
            to_obj = interaction.get('to', '')
            message = interaction.get('message', '')
            arrow = interaction.get('arrow', '->')
            
            mermaid += f"    {from_obj} {arrow} {to_obj}: {message}\n"
        
        return mermaid
    
    def generate_package_diagram_mermaid(self, modules: List[Dict[str, Any]]) -> str:
        """
        Генерация диаграммы пакетов в формате Mermaid
        
        Args:
            modules: Список модулей
            
        Returns:
            Mermaid диаграмма
        """
        mermaid = "graph TB\n"
        
        for module in modules:
            module_name = module.get('name', 'Unknown')
            module_id = module_name.replace('.', '_').replace('-', '_')
            
            mermaid += f"    {module_id}[\"{module_name}\"]\n"
            
            # Добавляем классы в модуле
            for cls in module.get('classes', []):
                cls_id = f"{module_id}_{cls['name']}"
                mermaid += f"    {cls_id}[\"{cls['name']}\"]\n"
                mermaid += f"    {module_id} --> {cls_id}\n"
        
        return mermaid
    
    def generate_architecture_diagram_mermaid(self, components: List[Dict[str, Any]]) -> str:
        """
        Генерация архитектурной диаграммы в формате Mermaid
        
        Args:
            components: Список компонентов системы
            
        Returns:
            Mermaid диаграмма
        """
        mermaid = "graph TB\n"
        
        # Группируем по типам
        layers = {}
        for component in components:
            comp_type = component.get('type', 'other')
            if comp_type not in layers:
                layers[comp_type] = []
            layers[comp_type].append(component)
        
        # Создаем слои
        for layer_name, layer_components in layers.items():
            mermaid += f"    subgraph {layer_name}\n"
            for comp in layer_components:
                comp_id = comp['name'].replace(' ', '_').replace('-', '_')
                comp_label = comp.get('label', comp['name'])
                mermaid += f"        {comp_id}[\"{comp_label}\"]\n"
            mermaid += "    end\n"
        
        # Добавляем связи
        for component in components:
            comp_id = component['name'].replace(' ', '_').replace('-', '_')
            for dep in component.get('dependencies', []):
                dep_id = dep.replace(' ', '_').replace('-', '_')
                mermaid += f"    {comp_id} --> {dep_id}\n"
        
        return mermaid
    
    def generate_plantuml_class_diagram(self, code_info: Dict[str, Any]) -> str:
        """
        Генерация диаграммы классов в формате PlantUML
        
        Args:
            code_info: Информация о коде
            
        Returns:
            PlantUML диаграмма
        """
        plantuml = "@startuml\n"
        
        for cls in code_info.get('classes', []):
            class_name = cls['name']
            plantuml += f"class {class_name} {{\n"
            
            # Атрибуты
            for attr in cls.get('attributes', []):
                plantuml += f"  + {attr}\n"
            
            # Методы
            for method in cls.get('methods', []):
                method_name = method['name']
                args = ', '.join([arg['name'] for arg in method.get('args', [])])
                plantuml += f"  + {method_name}({args})\n"
            
            plantuml += "}\n\n"
            
            # Наследование
            for base in cls.get('bases', []):
                base_name = base.split('.')[-1]
                plantuml += f"{base_name} <|-- {class_name}\n"
        
        plantuml += "@enduml\n"
        return plantuml

