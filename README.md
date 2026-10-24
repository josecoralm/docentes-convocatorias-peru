# 🎓 Docentes Convocatorias Perú - Universidades y Posgrado

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/josecoralm/docentes-convocatorias-peru)

Plataforma web integral y agregador inteligente para rastrear, centralizar y postular a todas las **convocatorias docentes universitarias y escuelas de posgrado en el Perú**.

---

## 🌟 Características Principales

1. **Cobertura Integral**:
   - **Universidades Públicas:** Concursos públicos de méritos (UNMSM, UNI, UNFV, UNALM, etc.) monitoreados vía *Talento Perú* y *Convocatorias de Trabajo*.
   - **Universidades Privadas de Élite:** Ulima, USIL, PUCP / CENTRUM, Universidad del Pacífico (PBS), ESAN, UPC, UTEC, Cayetano Heredia, etc.
   - **Escuelas de Posgrado & Maestrías:** Plazas para maestrías especializadas (MBA, Dirección de Operaciones, SCM, Finanzas, Gestión Pública).
   - **100% Remoto / Nivel Nacional:** Oportunidades de cátedra virtual para todo el Perú (Universidad Continental, USMP Virtual, programas a distancia).
   - **Portales de Empleo Integrados:** Computrabajo, HiringRoom, LinkedIn Jobs y bolsas oficiales de empleo.

2. **Scraping y Rastreos Automáticos en Vivo**:
   - Motor de web scrapers desarrollado en **Python (FastAPI + BeautifulSoup)** con deduplicación inteligente y normalización de vacantes.
   - Botón interactivo de **"Sincronizar Radar"** en la interfaz para actualizar plazas en tiempo real.

3. **Interfaz Web Moderna y Reactiva**:
   - Frontend en **React 18 + Tailwind CSS + Lucide Icons**.
   - Filtros instantáneos por:
     - *Nivel Académico* (Posgrado & Maestrías, Pregrado, Programas Adultos/CPEL/EPE).
     - *Tipo de Institución* (Pública vs. Privada).
     - *Modalidad* (Presencial Lima, Híbrido, 100% Virtual Nacional).
   - Ficha detallada con requisitos (Grado SUNEDU, experiencia requerida, tipo de contrato, fecha límite).
   - Enlace directo con un clic a las **bases oficiales** o al portal de postulación institucional.

4. **Herramientas para el Postulante**:
   - **Directorio de Bancos de Talento:** Acceso directo a los portales permanentes de contratación docente (Ulima Laboral, HiringRoom USIL, Bolsa UP, Krowdy UTP, etc.).
   - **Checklist SUNEDU & Guía Normativa:** Guía de requisitos según la Ley Universitaria N° 30220 (registro SUNEDU, legajo foliado vs. CV ejecutivo, clase modelo de 20 min).

---

## 🚀 Cómo Iniciar la Web

### Opción 1: Un Solo Comando (Recomendado)

Desde la terminal, ejecuta:
```bash
cd /Users/josecoral/.gemini/antigravity/scratch/docentes-convocatorias
./run.sh
```

Abre tu navegador en:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## ☁️ Despliegue en Render (En la Nube)

Esta plataforma está 100% lista para desplegarse gratis en **Render.com** (o Railway / Fly.io):

### Opción Rápida con Blueprint (`render.yaml`)
1. Sube este proyecto a tu cuenta de **GitHub**.
2. Ingresa a [dashboard.render.com](https://dashboard.render.com/) y haz clic en **New +** -> **Blueprint**.
3. Conecta tu repositorio de GitHub. Render detectará automáticamente el archivo `render.yaml` y configurará el build y start command.
4. Haz clic en **Apply** y en menos de 2 minutos tu aplicación estará pública en internet (ej: `https://docentes-convocatorias-peru.onrender.com`).

### Opción Manual en Render (Web Service)
1. En Render Dashboard, selecciona **New +** -> **Web Service**.
2. Conecta tu repositorio de GitHub.
3. Configura:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Selecciona el plan gratuito (**Free**) y haz clic en **Create Web Service**.

---

## 🛠️ Subir a GitHub paso a paso

```bash
# 1. En la carpeta del proyecto:
git init
git add .
git commit -m "feat: plataforma unificada de convocatorias docentes Perú"

# 2. Crea un repositorio en GitHub (ej: docentes-convocatorias-peru) y vincula:
git remote add origin https://github.com/TU-USUARIO/docentes-convocatorias-peru.git
git branch -M main
git push -u origin main
```

Si deseas modificar la interfaz y ver los cambios al instante con Vite:
```bash
# Terminal 1: Servidor Backend API
cd /Users/josecoral/.gemini/antigravity/scratch/docentes-convocatorias/backend
/Users/josecoral/.gemini/antigravity/scratch/venv/bin/python -m uvicorn main:app --reload --port 8000

# Terminal 2: Servidor Frontend Vite
cd /Users/josecoral/.gemini/antigravity/scratch/docentes-convocatorias/frontend
npm run dev
```

---

## 📁 Estructura del Código

```
docentes-convocatorias/
├── run.sh                          # Script de lanzamiento inmediato
├── README.md                       # Documentación completa
├── backend/                        # Backend API en Python FastAPI
│   ├── main.py                     # API REST, endpoints y servidor estático SPA
│   ├── models.py                   # Modelos de datos Pydantic
│   ├── database.py                 # Persistencia y lógica de consultas y filtros
│   ├── data/
│   │   └── convocatorias.json      # Base de datos centralizada de convocatorias
│   └── scrapers/
│       ├── base_scraper.py         # Interfaz base de scrapers
│       ├── computrabajo_scraper.py # Scraper de avisos en Computrabajo Perú
│       ├── convocatorias_trabajo_scraper.py # Scraper de universidades públicas
│       └── crawler_manager.py      # Orquestador y deduplicador de scrapers
└── frontend/                       # Aplicación React + Tailwind
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    └── src/
        ├── App.tsx                 # Dashboard principal con filtros, buscador y modales
        ├── types.ts                # Tipos TypeScript
        └── index.css               # Estilos y animaciones
```

---

## 📚 Endpoints de la API

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/` | Interfaz web de la plataforma |
| `GET` | `/api/convocatorias` | Listado con filtros (`q`, `tipo_institucion`, `nivel`, `modalidad`, `skip`, `limit`) |
| `GET` | `/api/convocatorias/{id}` | Ficha completa de una convocatoria |
| `GET` | `/api/stats` | Estadísticas globales (públicas, privadas, posgrado, modalidades) |
| `POST` | `/api/sync/sync-now` | Ejecución en vivo de los scrapers |
| `GET` | `/docs` | Documentación interactiva Swagger / OpenAPI |
