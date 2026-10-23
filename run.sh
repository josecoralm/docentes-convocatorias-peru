#!/bin/bash
# Script de inicio rápido de la Plataforma Radar Docente Convocatorias Perú

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$PROJECT_DIR/../venv/bin/python"

echo "🎓 Iniciando Radar de Convocatorias Docentes Universitarias (Perú)..."
echo "📂 Directorio del proyecto: $PROJECT_DIR"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "⚠️  Virtualenv no encontrado en $VENV_PYTHON, usando python3 global..."
    VENV_PYTHON="python3"
fi

cd "$PROJECT_DIR/backend"
echo "🚀 Levantando servidor FastAPI en http://localhost:8000 ..."
echo "🌐 Abre tu navegador en: http://localhost:8000 (o http://127.0.0.1:8000)"
"$VENV_PYTHON" -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
