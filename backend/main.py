from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional, List
import os
import uvicorn

from models import Convocatoria, ConvocatoriaCreate, FiltrosConvocatoria, StatsResponse
from database import query_convocatorias, get_stats, add_or_update_convocatoria, load_convocatorias
from scrapers.crawler_manager import CrawlerManager

app = FastAPI(
    title="Docentes Convocatorias Perú API",
    description="API de agregación y búsqueda de convocatorias docentes para universidades y posgrado en el Perú.",
    version="1.0.0"
)

# Permitir CORS para comunicación frontend Next.js / Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crawler_manager = CrawlerManager()

DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))

@app.get("/api/health")
def health():
    return {
        "app": "Radar de Convocatorias Docentes Universitarias (Perú)",
        "status": "online",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

@app.get("/api/convocatorias")
def get_convocatorias(
    q: Optional[str] = Query(None, description="Término de búsqueda libre"),
    tipo_institucion: Optional[str] = Query(None, description="Pública, Privada o Todos"),
    nivel: Optional[str] = Query(None, description="Posgrado, Pregrado o Todos"),
    modalidad: Optional[str] = Query(None, description="Presencial, Virtual, Híbrido o Todos"),
    institucion: Optional[str] = Query(None, description="Filtrar por universidad"),
    fuente: Optional[str] = Query(None, description="Filtrar por fuente / portal"),
    estado: Optional[str] = Query(None, description="Abierta, Banco Permanente, Próxima"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200)
):
    filtros = FiltrosConvocatoria(
        q=q,
        tipo_institucion=tipo_institucion,
        nivel=nivel,
        modalidad=modalidad,
        institucion=institucion,
        fuente=fuente,
        estado=estado,
        skip=skip,
        limit=limit
    )
    items, total = query_convocatorias(filtros)
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@app.get("/api/convocatorias/{convocatoria_id}", response_model=Convocatoria)
def get_convocatoria_detail(convocatoria_id: str):
    items = load_convocatorias()
    match = next((c for c in items if c["id"] == convocatoria_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    return Convocatoria(**match)

@app.get("/api/stats", response_model=StatsResponse)
def get_platform_stats():
    return get_stats()

@app.post("/api/sync")
def trigger_sync(background_tasks: BackgroundTasks):
    """Dispara los scrapers en segundo plano para traer nuevas vacantes de portales y universidades."""
    def run_sync_task():
        crawler_manager.run_all()

    background_tasks.add_task(run_sync_task)
    return {"message": "Sincronización de convocatorias iniciada en segundo plano"}

@app.post("/api/sync/sync-now")
def sync_now():
    """Ejecuta los scrapers sincrónicamente y retorna el reporte detallado."""
    result = crawler_manager.run_all()
    return result

@app.get("/api/universidades")
def get_universidades_list():
    items = load_convocatorias()
    unis = sorted(list(set(c["institucion"] for c in items)))
    return {"universidades": unis}

@app.get("/api/universidades-directorio")
def get_universidades_directorio():
    """Retorna el catálogo nacional de todas las universidades del Perú (públicas y privadas) con enlaces oficiales de postulación."""
    from database import load_universidades_directorio
    unis = load_universidades_directorio()
    return {
        "total": len(unis),
        "universidades": unis
    }

# Montar frontend estático si existe
if os.path.exists(DIST_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")

    @app.api_route("/", methods=["GET", "HEAD"])
    def serve_index():
        return FileResponse(os.path.join(DIST_DIR, "index.html"))

    @app.api_route("/{full_path:path}", methods=["GET", "HEAD"])
    def serve_spa(full_path: str):
        file_path = os.path.join(DIST_DIR, full_path)
        if full_path and os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(DIST_DIR, "index.html"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
