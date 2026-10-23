from typing import List, Optional
from pydantic import BaseModel, Field

class Convocatoria(BaseModel):
    id: str
    titulo: str
    institucion: str
    tipo_institucion: str  # "Pública", "Privada", "Escuela de Posgrado", "Instituto Superior"
    nivel: str             # "Posgrado", "Pregrado", "Educación Ejecutiva", "Pregrado y Posgrado"
    modalidad: str         # "Presencial", "Semipresencial / Híbrido", "100% Virtual / Remoto"
    ubicacion: str         # "Lima", "Arequipa", "Nacional Remoto", etc.
    facultad_o_carrera: str
    tipo_contrato: str     # "Tiempo Completo", "Tiempo Parcial", "Por Asignatura", "Concurso Público"
    remuneracion: Optional[str] = "Según categoría docente / Tarifario institucional"
    requisitos: List[str] = Field(default_factory=list)
    fecha_publicacion: str
    fecha_limite: str
    enlace_postulacion: str
    fuente: str            # "Portal Oficial", "Talento Perú", "Computrabajo", "HiringRoom", "LinkedIn"
    estado: str            # "Abierta", "Banco Permanente", "Próxima"
    descripcion: str
    contacto: Optional[str] = ""
    tags: List[str] = Field(default_factory=list)

class ConvocatoriaCreate(BaseModel):
    titulo: str
    institucion: str
    tipo_institucion: str
    nivel: str
    modalidad: str
    ubicacion: str
    facultad_o_carrera: str
    tipo_contrato: str
    remuneracion: Optional[str] = None
    requisitos: List[str] = Field(default_factory=list)
    fecha_limite: str
    enlace_postulacion: str
    fuente: str
    estado: str = "Abierta"
    descripcion: str
    contacto: Optional[str] = ""
    tags: List[str] = Field(default_factory=list)

class FiltrosConvocatoria(BaseModel):
    q: Optional[str] = None
    tipo_institucion: Optional[str] = None
    nivel: Optional[str] = None
    modalidad: Optional[str] = None
    institucion: Optional[str] = None
    fuente: Optional[str] = None
    estado: Optional[str] = None
    skip: int = 0
    limit: int = 50

class StatsResponse(BaseModel):
    total_convocatorias: int
    publicas: int
    privadas: int
    posgrado: int
    pregrado: int
    virtual_remoto: int
    presencial_lima: int
    por_institucion: dict
    por_fuente: dict
