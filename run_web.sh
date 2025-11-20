#!/bin/bash

echo "========================================"
echo "Doc-Gen-Finance35 Web Application"
echo "========================================"
echo ""
echo "Проверка установки..."
python3 --version
echo ""
echo "Установка зависимостей..."
pip install -r requirements.txt
echo ""
echo "Создание шаблонов..."
python3 templates/create_templates.py
echo ""
echo "Запуск веб-сервера..."
echo "Откройте в браузере: http://127.0.0.1:5000"
echo ""
python3 app.py

