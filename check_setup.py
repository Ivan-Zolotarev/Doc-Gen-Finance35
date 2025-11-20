"""
Скрипт для проверки установки и настройки проекта
"""

import sys
from pathlib import Path

def check_imports():
    """Проверка импортов модулей"""
    print("Проверка импортов...")
    try:
        from doc_generator import DocumentGenerator
        print("✓ Модуль doc_generator успешно импортирован")
        return True
    except ImportError as e:
        print(f"✗ Ошибка импорта: {e}")
        print("\nРешение:")
        print("1. Убедитесь, что вы находитесь в корневой директории проекта")
        print("2. Проверьте, что все файлы модуля doc_generator/ существуют")
        return False

def check_dependencies():
    """Проверка установленных зависимостей"""
    print("\nПроверка зависимостей...")
    required_packages = [
        'docx',
        'openpyxl',
        'fpdf',
        'jinja2',
        'pandas'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'docx':
                import docx
            elif package == 'fpdf':
                import fpdf
            else:
                __import__(package)
            print(f"✓ {package} установлен")
        except ImportError:
            print(f"✗ {package} не установлен")
            missing.append(package)
    
    if missing:
        print(f"\nНеобходимо установить: {', '.join(missing)}")
        print("Выполните: pip install -r requirements.txt")
        return False
    
    return True

def check_templates():
    """Проверка наличия шаблонов"""
    print("\nПроверка шаблонов...")
    templates_dir = Path("templates")
    required_templates = [
        "contract_template.docx",
        "report_template.docx",
        "certificate_template.docx"
    ]
    
    if not templates_dir.exists():
        print("✗ Директория templates/ не найдена")
        return False
    
    missing = []
    for template in required_templates:
        template_path = templates_dir / template
        if template_path.exists():
            print(f"✓ {template} найден")
        else:
            print(f"✗ {template} не найден")
            missing.append(template)
    
    if missing:
        print(f"\nНеобходимо создать шаблоны: {', '.join(missing)}")
        print("Выполните: python templates/create_templates.py")
        return False
    
    return True

def check_directories():
    """Проверка структуры директорий"""
    print("\nПроверка структуры проекта...")
    required_dirs = ["doc_generator", "templates", "output", "config", "data", "examples"]
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✓ {dir_name}/ существует")
        else:
            print(f"✗ {dir_name}/ не найдена")
            if dir_name == "output":
                dir_path.mkdir(exist_ok=True)
                print(f"  → Создана директория {dir_name}/")
    
    return True

def main():
    print("=" * 50)
    print("Проверка установки Doc-Gen-Finance35")
    print("=" * 50)
    
    all_ok = True
    
    # Проверка структуры
    check_directories()
    
    # Проверка импортов
    if not check_imports():
        all_ok = False
    
    # Проверка зависимостей
    if not check_dependencies():
        all_ok = False
    
    # Проверка шаблонов
    if not check_templates():
        all_ok = False
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✓ Все проверки пройдены успешно!")
        print("Проект готов к использованию.")
        print("\nЗапустите пример:")
        print("  python examples/basic_example.py")
    else:
        print("✗ Обнаружены проблемы")
        print("Исправьте ошибки и запустите проверку снова.")
    print("=" * 50)

if __name__ == "__main__":
    main()

