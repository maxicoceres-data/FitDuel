#!/bin/bash

echo ""
echo "🌿 Maxi & Belu - Streamlit Edition"
echo ""

# Verificar si existe venv
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar venv
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -q -r requirements.txt

# Ejecutar Streamlit
echo ""
echo "✅ ¡Listo! Abriendo la aplicación..."
echo ""
streamlit run inicio.py
