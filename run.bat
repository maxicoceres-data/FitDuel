@echo off
echo.
echo 🌿 Maxi & Belu - Streamlit Edition
echo.

REM Verificar si existe venv
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar venv
call venv\Scripts\activate

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt -q

REM Ejecutar Streamlit
echo.
echo ✅ ¡Listo! Abriendo la aplicación...
echo.
streamlit run inicio.py

pause
