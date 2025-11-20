@echo off
echo ========================================
echo Doc-Gen-Finance35 Web Application
echo ========================================
echo.
echo Проверка установки...
python --version
echo.
echo Установка зависимостей...
pip install -r requirements.txt
echo.
echo Создание шаблонов...
python templates/create_templates.py
echo.
echo Запуск веб-сервера...
echo Откройте в браузере: http://127.0.0.1:5000
echo.
python app.py
pause

